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
from django.contrib.auth.models import User, Group, Permission
from django.contrib.auth.decorators import login_required
from .decorators import supplier_required, client_required
from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.apps import apps
from oscar.core.loading import get_model
from django.views import generic
from django.contrib.contenttypes.models import ContentType

Partner = get_model('partner', 'Partner')

# Registro Cliente API
class ClientRegisterView(generics.CreateAPIView):
    queryset = ClientProfile.objects.all()
    serializer_class = ClientSerializer

# Registro Fornecedor (Web)
class SupplierRegisterView(FormView):
    template_name = 'registration/register_supplier.html'
    form_class = SuplierRegisterForm
    success_url = '/dashboard/'

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

        # Criar Partner no Oscar
        partner = Partner.objects.create(name=form.cleaned_data['company_name'])
        partner.users.add(user)

        # Adicionar permissão partner.dashboard_access
        content_type = ContentType.objects.get(app_label='partner', model='partner')
        permission = Permission.objects.get(content_type=content_type, codename='dashboard_access')
        user.user_permissions.add(permission)

        # Atribuir ao grupo Fornecedor
        group, created = Group.objects.get_or_create(name='Fornecedor')
        user.groups.add(group)

        # Autenticar e logar o usuário
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

                # Redirecionamento baseado no tipo de usuário
                if hasattr(user, 'suplier_profile'):
                    return redirect('/dashboard/')
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

# View Dashboard Fornecedor (protegida) - você pode manter para personalizar depois
@supplier_required
def supplier_dashboard(request):
    return render(request, 'supplier/dashboard.html')

# View Dashboard Cliente (protegida) - você pode manter para personalizar depois
@client_required
def client_dashboard(request):
    return render(request, '/')

def order_progress(request):
    return render(request, 'oscar/customer/order/order_progress_list.html')
