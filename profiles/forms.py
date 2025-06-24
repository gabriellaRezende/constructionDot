# profiles/forms.py
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import ClientProfile, SuplierProfile

class ClientRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(label="Full Name", required=True)
    contact_phone = forms.CharField(label="Phone", required=True)
    delivery_address = forms.CharField(label="Delivery Address", required=True)
    city_code = forms.CharField(label="City Code", required=False)
    nif = forms.CharField(label="NIF", required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        if commit:
            user.save()
            ClientProfile.objects.create(
                user=user,
                contact_phone=self.cleaned_data['contact_phone'],
                delivery_address=self.cleaned_data['delivery_address'],
                city_code=self.cleaned_data.get('city_code', ''),
                nif=self.cleaned_data['nif']
            )
        return user


class SuplierRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(label="Full Name", required=True)
    company_name = forms.CharField(label="Company Name", required=True)
    contact_phone = forms.CharField(label="Contact Phone", required=True)
    company_address = forms.CharField(label="Company Address", required=True)
    cnpj = forms.CharField(label="CNPJ", required=True)
    ie = forms.CharField(label="State Registration", required=False)

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        if commit:
            user.save()
            SuplierProfile.objects.create(
                user=user,
                company_name=self.cleaned_data['company_name'],
                contact_phone=self.cleaned_data['contact_phone'],
                company_address=self.cleaned_data['company_address'],
                cnpj=self.cleaned_data['cnpj'],
                ie=self.cleaned_data.get('ie', '')
            )
        return user