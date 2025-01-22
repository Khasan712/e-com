"""
In this file need to write all querysets for import function
"""

# Order app tables   ===================================================
from v1.order.models import Order, OrderItem


def get_order_queryset():
    return Order.objects.order_by('-id')


def get_order_item_queryset():
    return OrderItem.objects.order_by('-id')


# Product app tables ===================================================
from v1.product.models import (
    Product, Category, Brand, Country, ProductItem, CharacterItem, Model, Characteristic,
    Barcode, Ikpu, Sku, ProductItemSellPrice, ProductItemDiscountPrice, TopCategory, TopProductItem, 
    MainBanner, AdsProductItem, Cart
)


def get_cart_queryset():
    return Cart.objects.order_by('-id')


def get_ads_product_item_queryset():
    return AdsProductItem.objects.order_by("-id")


def get_main_banner_queryset():
    return MainBanner.objects.order_by("-id")


def get_top_product_queryset():
    return TopProductItem.objects.order_by("-id")


def get_top_category_queryset():
    return TopCategory.objects.order_by("-id")


def get_barcode_queryset():
    return Barcode.objects.order_by("-id")


def get_ikpu_queryset():
    return Ikpu.objects.order_by("-id")


def get_sku_queryset():
    return Sku.objects.order_by("-id")


def get_product_item_sell_price_queryset():
    return ProductItemSellPrice.objects.order_by("-id")


def get_product_item_discount_price_queryset():
    return ProductItemDiscountPrice.objects.order_by("-id")


def get_category_queryset():
    return Category.objects.order_by("-id")


def get_product_queryset():
    return Product.objects.order_by("-id")


def get_brand_queryset():
    return Brand.objects.order_by("-id")


def get_country_queryset():
    return Country.objects.order_by("-id")


def get_product_item_queryset():
    return ProductItem.objects.order_by("-id")


def get_characteristic_queryset():
    return Characteristic.objects.order_by("-id")


def get_character_item_queryset():
    return CharacterItem.objects.order_by("-id")


def get_model_queryset():
    return Model.objects.order_by("-id")


# User app tables =======================================================
from v1.user.models import (
    User,
    Seller,
    Admin,
    Client
)


def get_user_queryset():
    return User.objects.order_by("-id")


def get_seller_queryset():
    return Seller.objects.order_by("-id")


def get_admin_queryset():
    return Admin.objects.order_by("-id")


def get_client_queryset():
    return Client.objects.order_by("-id")


# Proposal app tables =======================================================
from v1.proposal.models import (
    Proposal,
)


def get_proposal_queryset():
    return Proposal.objects.order_by('-id')
