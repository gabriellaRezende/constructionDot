from django.urls import path
from .views import ClientRegisterView, SuplierRegisterView

urlpatterns = [
    path('register/cliente/', ClientRegisterView.as_view(), name='client_register'),
    path('register/fornecedor/', SuplierRegisterView.as_view(), name='suplier_register'),
]
