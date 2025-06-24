from django.urls import path
from .views import LoginRegisterClientView, SupplierRegisterView, supplier_dashboard

urlpatterns = [
    path('accounts/login/', LoginRegisterClientView.as_view(), name='login'),
    path('supplier/register/', SupplierRegisterView.as_view(), name='supplier_register'),
    path('supplier/dashboard/', supplier_dashboard, name='supplier_dashboard'),
]
