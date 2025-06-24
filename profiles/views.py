from django.shortcuts import render

# profiles/views.py
from django.urls import reverse_lazy
from django.views.generic import CreateView
from .forms import ClientRegisterForm, SuplierRegisterForm

class ClientRegisterView(CreateView):
    form_class = ClientRegisterForm
    template_name = 'registration/client_register.html'
    success_url = reverse_lazy('login')


class SuplierRegisterView(CreateView):
    form_class = SuplierRegisterForm
    template_name = 'registration/suplier_register.html'
    success_url = reverse_lazy('login')