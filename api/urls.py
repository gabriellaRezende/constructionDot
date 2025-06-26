from django.urls import path
from .views import (
    ProductListView, ProductDetailView, ProductCreateView, ProductUpdateView, ProductDeleteView,
    OrderListView, OrderDetailView, OrderCreateView,
    RegisterClientView, RegisterSuplierView, LoginView,
    ProfileView,
    CategoryListView,
)

urlpatterns = [
    # Produtos
    path('produtos/', ProductListView.as_view(), name='product-list'),
    path('produtos/<int:pk>/', ProductDetailView.as_view(), name='product-detail'),
    path('produtos/criar/', ProductCreateView.as_view(), name='product-create'),
    path('produtos/<int:pk>/atualizar/', ProductUpdateView.as_view(), name='product-update'),
    path('produtos/<int:pk>/deletar/', ProductDeleteView.as_view(), name='product-delete'),

    # Encomendas
    path('encomendas/', OrderListView.as_view(), name='order-list'),
    path('encomendas/criar/', OrderCreateView.as_view(), name='order-create'),
    path('encomendas/<int:pk>/', OrderDetailView.as_view(), name='order-detail'),

    # Autenticação e registro
    path('register/cliente/', RegisterClientView.as_view(), name='register-client'),
    path('register/fornecedor/', RegisterSuplierView.as_view(), name='register-suplier'),
    path('login/', LoginView.as_view(), name='login'),

    # Perfil
    path('profile/', ProfileView.as_view(), name='profile'),

    # Categorias
    path('categorias/', CategoryListView.as_view(), name='category-list'),
]
