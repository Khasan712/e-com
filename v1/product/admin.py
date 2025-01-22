from django.contrib import admin
from .models import (
    Category, Brand, Country, Product, CharacterItem, Characteristic, ProductItem, ProductItemImage,
    AdsProductItem, TopProductItem, Model, Barcode, Ikpu, Sku, ProductItemSellPrice, ProductItemDiscountPrice,
    TopCategory, MainBanner, Cart
)


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ("id", "product", "quantity", 'user', 'created_at', 'is_active', 'is_deleted')


@admin.register(TopProductItem)
class TopProductItemAdmin(admin.ModelAdmin):
    list_display = ("id", "product_item", 'created_at', 'is_active', 'is_deleted')


@admin.register(AdsProductItem)
class AdsProductItemAdmin(admin.ModelAdmin):
    list_display = ("id", "product_item", "order_num", 'created_at', 'is_active', 'is_deleted')


admin.site.register(MainBanner)


@admin.register(TopCategory)
class TopCategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "category", "images")


@admin.register(Barcode)
class BarcodeAdmin(admin.ModelAdmin):
    list_display = ("id", "code", "title", 'created_at', 'is_active', 'is_deleted')


@admin.register(Ikpu)
class IkpuAdmin(admin.ModelAdmin):
    list_display = ("id", "code", 'created_at', 'is_active', 'is_deleted')


@admin.register(Sku)
class SkuAdmin(admin.ModelAdmin):
    list_display = ("id", "seller", "sku", 'created_at', 'is_active', 'is_deleted')


@admin.register(ProductItemSellPrice)
class ProductItemSellPriceAdmin(admin.ModelAdmin):
    list_display = ("id", "product_item", "price", 'created_at', 'is_active', 'is_deleted')


@admin.register(ProductItemDiscountPrice)
class ProductItemDiscountPriceAdmin(admin.ModelAdmin):
    list_display = ("id", "product_item", "price", 'created_at', 'is_active', 'is_deleted')


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'title_ln', 'parent', 'created_at')


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ("id", 'title_ln', 'created_at', 'is_active', 'is_deleted')


@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = ("id", 'title_ln', 'created_at', 'is_active', 'is_deleted')


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'title_ln', 'category', 'seller', 'is_deleted', 'is_active'
    )


@admin.register(CharacterItem)
class CharacterItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'title_ln', 'value', 'parent', 'created_at', 'is_deleted', 'is_active')


@admin.register(Characteristic)
class CharacteristicAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'product', 'parent', 'created_at', 'is_deleted', 'is_active')


@admin.register(ProductItem)
class ProductItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'artikul_ln', 'product', 'barcode', 'ikpu', 'status', 'created_at', 'is_deleted', 'is_active')
    raw_id_fields = ("ikpu", 'characteristics')


@admin.register(ProductItemImage)
class ProductItemImageAdmin(admin.ModelAdmin):
    list_display = ('id', 'product', 'characteristic', 'created_at', 'is_deleted', 'is_active')


@admin.register(Model)
class ModelAdmin(admin.ModelAdmin):
    list_display = ("id", "title_ln", "title_ru", "brand", "created_at")
