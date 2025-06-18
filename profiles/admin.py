from django.contrib import admin
from .models import SuplierProfile, ClientProfile

@admin.register(SuplierProfile)
class SuplierProfileAdmin(admin.ModelAdmin):
    list_display = ('company_name', 'user', 'cnpj')
    search_fields = ('company_name', 'user__username', 'cnpj')

@admin.register(ClientProfile)
class ClientProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'contact_phone', 'is_preferred_client')
    search_fields = ('user__username', 'nif')

    
# Register your models here. 
