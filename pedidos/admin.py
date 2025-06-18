from django.contrib import admin
from .models import Order, OrderItem

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'client', 'create_at', 'status', 'total')
    search_fields = ('client__user__username',)
    list_filter = ('status', 'create_at')

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'product', 'quantity', 'unity_price', 'supplier')
    search_fields = ('order__id', 'product__name')
    list_filter = ('supplier', 'product')

# Register your models here.
