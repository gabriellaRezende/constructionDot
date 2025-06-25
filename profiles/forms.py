from django import forms
from django.core.exceptions import ValidationError
from .models import SuplierProfile
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

User = get_user_model()

class SupplierRegisterForm(forms.Form):
    # campos de User
    username = forms.CharField(max_length=150)
    email    = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)

    # campos de perfil
    company_name    = forms.CharField(max_length=100)
    contact_phone   = forms.CharField(max_length=20)
    company_address = forms.CharField(max_length=255)
    cnpj            = forms.CharField(max_length=18)
    ie              = forms.CharField(max_length=30, required=False)

    def clean_cnpj(self):
        cnpj = self.cleaned_data['cnpj']
        if SuplierProfile.objects.filter(cnpj=cnpj).exists():
            raise ValidationError("Este CNPJ já está cadastrado.")
        return cnpj

    def save(self):
        # Cria o User
        user = User.objects.create_user(
            username=self.cleaned_data['username'],
            email=self.cleaned_data['email'],
            password=self.cleaned_data['password'],
        )

        from django.contrib.auth.models import Group
        fornecedor_group, _ = Group.objects.get_or_create(name='Fornecedor')
        user.groups.add(fornecedor_group)

        SuplierProfile.objects.create(
            user=user,
            company_name=self.cleaned_data['company_name'],
            contact_phone=self.cleaned_data['contact_phone'],
            company_address=self.cleaned_data['company_address'],
            cnpj=self.cleaned_data['cnpj'],
            ie=self.cleaned_data.get('ie', '')
        )
        return user
