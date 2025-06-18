from django.conf import settings
from django.db import models

# Create your models here.

class SuplierProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='suplier_profile'
    )
    company_name = models.CharField("Company Name", max_length=255)
    contact_phone = models.CharField("Contact Phone", max_length=20)
    company_address = models.CharField("Company Address", max_length=255)
    cnpj = models.CharField("CNPJ", max_length=20, unique=True)
    ie = models.CharField("State Registration", max_length=30, blank=True)

    def __str__(self):
        return f"{self.company_name} - {self.user.username}"
    
class ClientProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='client_profile'
    )
    contact_phone = models.CharField("Phone", max_length=20)
    delivery_address = models.CharField("Delivery Address", max_length=255)
    city_code = models.CharField("City Code", max_length=10, blank=True)
    nif = models.CharField("NIF", max_length=20, unique=True)
    is_preferred_client = models.BooleanField("Preferred Client", default=False) # indica que o cliente é preferencial, porem apenas o admin pode alterar essa flag
    

    def __str__(self):
        return f"Client: {self.user.username}"