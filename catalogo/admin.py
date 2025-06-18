from django.contrib import admin
from .models import Category
from .models import Product

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'parent')
    prepopulated_fields = {'slug': ('name',)}
    list_filter = ('parent',)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'in_stock', 'supplier', 'Category')
    search_fields = ('name', 'description')
    list_filter = ('name', 'description')


