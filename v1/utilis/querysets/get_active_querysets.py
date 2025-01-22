# Order app tables   ===================================================
from .get_queries import get_order_queryset, get_order_item_queryset


def get_active_orders():
    return get_order_queryset().filter(is_active=True, is_deleted=False)


def get_active_order_items():
    return get_order_item_queryset().filter(is_active=True, is_deleted=False)


# Product app tables =====================================================
from .get_queries import (
    get_brand_queryset, get_category_queryset, get_country_queryset, get_product_queryset, get_product_item_queryset,
    get_character_item_queryset, get_model_queryset, get_characteristic_queryset, get_barcode_queryset, get_ikpu_queryset,
    get_sku_queryset, get_product_item_sell_price_queryset, get_top_category_queryset, get_top_product_queryset, 
    get_main_banner_queryset, get_ads_product_item_queryset, get_cart_queryset
)


def get_active_cart():
    return get_cart_queryset().filter(is_active=True, is_deleted=False)


def get_active_ads_product_items():
    return get_ads_product_item_queryset().filter(is_active=True, is_deleted=False)


def get_active_main_banner():
    return get_main_banner_queryset().filter(is_active=True, is_deleted=False)

def get_active_top_product():
    return get_top_product_queryset().filter(is_active=True, is_deleted=False)

def get_active_top_category():
    return get_top_category_queryset().filter(is_active=True, is_deleted=False)

def get_active_product_item_sell_price():
    return get_product_item_sell_price_queryset().filter(is_active=True, is_deleted=False)

def get_active_sku():
    return get_sku_queryset().filter(is_active=True, is_deleted=False)

def get_active_ikpu():
    return get_ikpu_queryset().filter(is_active=True, is_deleted=False)

def get_active_barcode():
    return get_barcode_queryset().filter(is_active=True, is_deleted=False)

def get_active_category_queryset():
    return get_category_queryset().filter(is_active=True, is_deleted=False)

def get_active_product_queryset():
    return get_product_queryset().filter(is_active=True, is_deleted=False)

def get_active_brands():
    return get_brand_queryset().filter(is_active=True, is_deleted=False)

def get_active_countries():
    return get_country_queryset().filter(is_active=True, is_deleted=False)

def get_active_product_items():
    return get_product_item_queryset().filter(is_active=True, is_deleted=False)

def get_active_characteristics():
    return get_characteristic_queryset().filter(is_active=True, is_deleted=False)

def get_active_character_items():
    return get_character_item_queryset().filter(is_active=True, is_deleted=False)

def get_active_models():
    return get_model_queryset().filter(is_active=True, is_deleted=False)


# User app tables ========================================================
from .get_queries import (
    get_user_queryset,
    get_seller_queryset,
    get_admin_queryset,
    get_client_queryset
)

def get_active_users():
    return get_user_queryset().filter(is_active=True, is_deleted=False)

def get_active_sellers():
    return get_seller_queryset().filter(is_active=True, is_deleted=False)

def get_active_admins():
    return get_admin_queryset().filter(is_active=True, is_deleted=False)

def get_active_clients():
    return get_client_queryset().filter(is_active=True, is_deleted=False)

def get_active_not_confirmed_clients():
    return get_active_clients().filter(is_confirmed=False)


# Propsal app tables ========================================================
from .get_queries import (
    get_proposal_queryset
)

def get_active_proposals():
    return get_proposal_queryset().filter(is_active=True, is_deleted=False)

