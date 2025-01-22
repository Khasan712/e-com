from django.contrib import admin
from .models import (
    ImportToWarehouseCart,
    Warehouse,
    ImportProductToWarehouse,
    ProductInWarehouse,
    ImportPriceProductInWarehouse,
    SellPriceProductInWarehouse,
    ImportQuantityProductInWarehouse,
    QuantityProductInWarehouse
)


@admin.register(ImportToWarehouseCart)
class ImportToWarehouseCartAdmin(admin.ModelAdmin):
    list_display = ("id", 'warehouse', 'seller', 'created_at', 'is_active', 'is_deleted')


@admin.register(Warehouse)
class WarehouseAdmin(admin.ModelAdmin):
    list_display = ("id", 'title', 'is_active', 'is_deleted')


@admin.register(ImportProductToWarehouse)
class ImportProductToWarehouseAdmin(admin.ModelAdmin):
    list_display = ('id', 'import_to_warehouse_cart', 'product', 'is_active', 'is_deleted', 'created_at')


@admin.register(ProductInWarehouse)
class ProductInWarehouseAdmin(admin.ModelAdmin):
    list_display = ("id", 'product', 'warehouse', 'seller', 'is_active', 'is_deleted', 'created_at')


@admin.register(ImportPriceProductInWarehouse)
class ImportPriceProductInWarehouseAdmin(admin.ModelAdmin):
    list_display = ('id', 'import_product_to_warehouse', 'product_in_warehouse', 'linked_characteristic', 'import_price')


@admin.register(SellPriceProductInWarehouse)
class SellPriceProductInWarehouseAdmin(admin.ModelAdmin):
    list_display = ('id', 'product_in_warehouse', 'linked_characteristic', 'price')


@admin.register(ImportQuantityProductInWarehouse)
class ImportQuantityProductInWarehouseAdmin(admin.ModelAdmin):
    list_display = ('id', 'import_product_to_warehouse', 'product_in_warehouse', 'linked_characteristic', 'quantity')


@admin.register(QuantityProductInWarehouse)
class QuantityProductInWarehouseAdmin(admin.ModelAdmin):
    list_display = ('id', 'product_in_warehouse', 'linked_characteristic', 'quantity')

