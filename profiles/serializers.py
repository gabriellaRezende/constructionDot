from rest_framework import serializers
from django.contrib.auth.models import User
from .models import ClientProfile, SuplierProfile

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClientProfile
        fields = '__all__'

class SupplierSerializer(serializers.ModelSerializer):
    class Meta:
        model = SuplierProfile
        fields = '__all__'
