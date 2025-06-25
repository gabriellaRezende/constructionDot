from rest_framework import generics
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from .models import ClientProfile, SuplierProfile
from .serializers import ClientSerializer, SupplierSerializer, UserSerializer
from django.views.generic.edit import FormView
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import ClientRegisterForm, SuplierRegisterForm
from django.contrib.auth.models import User, Group
from django.contrib.auth.decorators import login_required
from .decorators import supplier_required, client_required
from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.apps import apps
from oscar.core.loading import get_model
from django.views import generic

# Registro Cliente API
class ClientRegisterView(generics.CreateAPIView):
    queryset = ClientProfile.objects.all()
    serializer_class = ClientSerializer

# Registro Fornecedor (Web)
class SupplierRegisterView(FormView):
    template_name = 'registration/register_supplier.html'
    form_class = SuplierRegisterForm
    success_url = '/supplier/dashboard/'

    def form_valid(self, form):
        username = form.cleaned_data['username']
        email = form.cleaned_data['email']
        password = form.cleaned_data['password1']

        # Criar usuário se não existir
        user, created = User.objects.get_or_create(username=username, defaults={'email': email})
        if created:
            user.set_password(password)
            user.save()
        else:
            form.add_error('username', 'Usuário já existe.')
            return self.form_invalid(form)

        # Verificar se já existe perfil de fornecedor
        if hasattr(user, 'suplier_profile'):
            form.add_error(None, 'Perfil de fornecedor já criado para este usuário.')
            return self.form_invalid(form)

        # Criar perfil fornecedor
        SuplierProfile.objects.create(
            user=user,
            company_name=form.cleaned_data['company_name'],
            contact_phone=form.cleaned_data['contact_phone'],
            company_address=form.cleaned_data['company_address'],
            cnpj=form.cleaned_data['cnpj'],
            ie=form.cleaned_data['ie']
        )

        # Atribuir ao grupo Fornecedor
        group, created = Group.objects.get_or_create(name='Fornecedor')
        user.groups.add(group)


        # Autenticar e logar o usuário com backend definido
        user_auth = authenticate(username=username, password=password)
        if user_auth is not None:
            auth_login(self.request, user_auth, backend='django.contrib.auth.backends.ModelBackend')
        else:
            form.add_error(None, 'Erro ao autenticar usuário após registro.')
            return self.form_invalid(form)

        return super().form_valid(form)


# Página combinada de Login + Registo Cliente
class LoginRegisterClientView(FormView):
    template_name = 'registration/login.html'
    form_class = ClientRegisterForm
    success_url = '/'

    def get(self, request, *args, **kwargs):
        login_form = AuthenticationForm()
        register_form = self.form_class()
        return render(request, self.template_name, {
            'login_form': login_form,
            'register_form': register_form
        })

    def post(self, request, *args, **kwargs):
        login_form = AuthenticationForm(data=request.POST)
        register_form = self.form_class(request.POST)

        if 'login' in request.POST:
            if login_form.is_valid():
                user = login_form.get_user()
                auth_login(request, user, backend='django.contrib.auth.backends.ModelBackend')

                # Verificar tipo de usuário
                if hasattr(user, 'suplier_profile'):
                    return redirect('/supplier/dashboard/')
                elif hasattr(user, 'client_profile'):
                    return redirect('/')
                else:
                    messages.error(request, 'Usuário sem perfil associado.')
                    return redirect('/')

            return render(request, self.template_name, {
                'login_form': login_form,
                'register_form': register_form
            })

        elif 'register' in request.POST:
            if register_form.is_valid():
                user = register_form.save()
                user.backend = 'django.contrib.auth.backends.ModelBackend'

                if not hasattr(user, 'client_profile'):
                    ClientProfile.objects.create(
                        user=user,
                        contact_phone=register_form.cleaned_data['contact_phone'],
                        delivery_address=register_form.cleaned_data['delivery_address'],
                        city_code=register_form.cleaned_data.get('city_code', ''),
                        nif=register_form.cleaned_data['nif']
                    )

                # Atribuir ao grupo Cliente
                group, created = Group.objects.get_or_create(name='Cliente')
                user.groups.add(group)


                auth_login(request, user, backend='django.contrib.auth.backends.ModelBackend')
                return redirect(self.success_url)

            return render(request, self.template_name, {
                'login_form': login_form,
                'register_form': register_form
            })

        return render(request, self.template_name, {
            'login_form': login_form,
            'register_form': register_form
        })


# View Sem Permissão
def sem_permissao(request):
    return render(request, 'sem_permissao.html')


# View Dashboard Fornecedor (protegida)
@supplier_required
def supplier_dashboard(request):
    return render(request, 'supplier/dashboard.html')


# View Dashboard Cliente (protegida)
@client_required
def client_dashboard(request):
    return render(request, '/')

Order = get_model('order', 'Order')

class OrderProgressView(LoginRequiredMixin, generic.ListView):
    """
    Custom order history view with progress bar.
    """
    model = Order
    template_name = "oscar/customer/order/order_progress_list.html"
    context_object_name = "orders"
    paginate_by = settings.OSCAR_ORDERS_PER_PAGE

    def get_queryset(self):
        """
        Return only orders from the logged-in user.
        """
        return self.model._default_manager.filter(user=self.request.user).order_by('-date_placed')