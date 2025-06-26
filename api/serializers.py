from rest_framework import serializers
from oscar.apps.catalogue.models import Product, Category
from oscar.apps.order.models import Order
from django.contrib.auth import get_user_model
from .models import SuplierProfile, ClientProfile

User = get_user_model()

# Serializer Produto
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'title', 'description', 'upc', 'structure', 'date_created']

# Serializer Categoria
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug']

# Serializer Encomenda
class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['id', 'number', 'date_placed', 'status', 'total_incl_tax']

# Serializer Usuário para registro e perfil
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']

# Serializer para Supplier Profile
class SuplierProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = SuplierProfile
        fields = ['user', 'company_name', 'contact_phone', 'company_address', 'cnpj', 'ie']

# Serializer para Client Profile
class ClientProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = ClientProfile
        fields = ['user', 'contact_phone', 'delivery_address', 'city_code', 'nif', 'is_preferred_client']
