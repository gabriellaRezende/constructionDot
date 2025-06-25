from django.urls import path
from . import views

urlpatterns = [
    path('supplier/produtos/', views.produto_list, name='produto_list'),
    path('supplier/produtos/novo/', views.produto_create, name='produto_create'),
    path('supplier/produtos/<int:pk>/editar/', views.produto_update, name='produto_update'),
    path('supplier/produtos/<int:pk>/excluir/', views.produto_delete, name='produto_delete'),
]

