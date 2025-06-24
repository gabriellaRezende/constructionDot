from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import SuplierProfile, ClientProfile

class SuplierRegisterForm(UserCreationForm):
    company_name = forms.CharField(max_length=255)
    contact_phone = forms.CharField(max_length=20)
    company_address = forms.CharField(max_length=255)
    cnpj = forms.CharField(max_length=20)
    ie = forms.CharField(max_length=30, required=False)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit)
        SuplierProfile.objects.create(
            user=user,
            company_name=self.cleaned_data['company_name'],
            contact_phone=self.cleaned_data['contact_phone'],
            company_address=self.cleaned_data['company_address'],
            cnpj=self.cleaned_data['cnpj'],
            ie=self.cleaned_data['ie']
        )
        return user

class ClientRegisterForm(UserCreationForm):
    contact_phone = forms.CharField(max_length=20)
    delivery_address = forms.CharField(max_length=255)
    city_code = forms.CharField(max_length=10, required=False)
    nif = forms.CharField(max_length=20)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit)
        ClientProfile.objects.create(
            user=user,
            contact_phone=self.cleaned_data['contact_phone'],
            delivery_address=self.cleaned_data['delivery_address'],
            city_code=self.cleaned_data['city_code'],
            nif=self.cleaned_data['nif']
        )
        return user