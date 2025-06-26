from django.db import models
from profiles.models import SuplierProfile, ClientProfile

class ApiAccessLog(models.Model):
    profile = models.ForeignKey(SuplierProfile, on_delete=models.CASCADE)
    accessed_at = models.DateTimeField(auto_now_add=True)
    endpoint = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.profile} accessed {self.endpoint} at {self.accessed_at}"

# Create your models here.

