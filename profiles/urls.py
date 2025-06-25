from django.urls import path
from .views import LoginRegisterClientView, SupplierRegisterView, supplier_dashboard, sem_permissao, OrderProgressView

urlpatterns = [
    path('sem-permissao/', sem_permissao, name='sem-permissao'),
    path('accounts/login/', LoginRegisterClientView.as_view(), name='login'),
    path('supplier/register/', SupplierRegisterView.as_view(), name='supplier_register'),
    path('supplier/dashboard/', supplier_dashboard, name='supplier_dashboard'),
    path('orders/progress/', OrderProgressView.as_view(), name='order-progress'),
]
