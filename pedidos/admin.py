from django.contrib import admin

# pedidos/admin.py
from django.contrib import admin
from .models import Encomenda, EncomendaItem

admin.site.register(Encomenda)
admin.site.register(EncomendaItem)