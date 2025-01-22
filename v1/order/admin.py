from django.contrib import admin
from v1.order.models import Order, OrderItem


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "status", 'created_at', 'is_active', 'is_deleted')


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ("id", "product", 'quantity', 'cart', 'created_at', 'is_active', 'is_deleted')


