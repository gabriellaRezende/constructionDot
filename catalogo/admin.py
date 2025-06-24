from django.contrib import admin

# catalogo/admin.py
from django.contrib import admin
from .models import Categoria, Produto

admin.site.register(Categoria)
admin.site.register(Produto)
