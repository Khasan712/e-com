import itertools

from celery import shared_task
from django.db import connection, transaction

from v1.product.models import Characteristic, ProductItem, Cart
from v1.services.minio_connect import product_upload_images
from v1.services.moysklad.create_product import create_product_moy_sklad
from v1.utilis.querysets.get_active_querysets import get_active_characteristics, get_active_product_queryset, \
    get_active_product_item_sell_price


@shared_task()
def upload_image_to_minio(files, product_id):
    product = get_active_product_queryset().get(id=product_id)
    images = product_upload_images(files, "BUCKET1")
    if not images:
        return {"status": False, "message": "Failed to upload images"}

    product.images += images
    product.save()
    return {"status": True, "message": "Image uploaded successfully"}


def create_product_item(args):
    result, product_id = args

    product_item = ProductItem.objects.create(product_id=product_id)
    characteristics_obj = get_active_characteristics().filter(id__in=result)

    product_item.characteristics.set(characteristics_obj)

    artikul_ln = characteristics_obj.values_list("title__title_ln", flat=True)
    artikul_ru = characteristics_obj.values_list("title__title_ru", flat=True)

    product_item.artikul_ln = ", ".join(artikul_ln)
    product_item.artikul_ru = ", ".join(artikul_ru)
    product_item.save()
    return f"{', '.join(artikul_ln)}"


def create_characteristics_value(args):
    characteristic, product_id = args
    characteristic_obj = Characteristic(
        title_id=characteristic['id'],
        product_id=product_id
    )
    characteristic_obj.save()

    with transaction.atomic():
        characteristic_value_objs = [
            Characteristic(
                title_id=characteristic_value,
                product_id=product_id,
                parent=characteristic_obj
            ) for characteristic_value in characteristic["values"]
        ]
        Characteristic.objects.bulk_create(characteristic_value_objs)
    return [obj.id for obj in characteristic_value_objs]


def characteristics_create(characteristics, product_id):
    values = []
    args = [(characteristic, product_id) for characteristic in characteristics]
    values += list(map(create_characteristics_value, args))

    combinations = list(itertools.product(*values))

    product_item_artikul = []
    args = [(list(combination), product_id) for combination in combinations]
    product_item_artikul += list(map(create_product_item, args))
    return product_item_artikul


def push_to_moysklad(product_item_artikul, product):

    moy_sklad_list = [
        {
            'name': product.title_ln,
            'artikul': product_item
        } for product_item in product_item_artikul
    ]

    id_list = create_product_moy_sklad(moy_sklad_list)

    for item in product.product_card.all():
        item.moy_sklad_id = id_list[0]['id']
        item.barcode = id_list[0]['barcode']
        item.json_data = id_list[0]['json_data']
        item.save()
        id_list.pop(0)


@shared_task()
def product_task(product_id, characteristics=None):
    """
    This task first of all creates characteristics, product_items and then
    creates product item in moysklad.ru platform
    """
    product_item_artikul = []
    product = get_active_product_queryset().get(id=product_id)
    if characteristics:
        product_item_artikul += characteristics_create(characteristics, product_id)
    else:
        product_item = ProductItem.objects.create(
            product_id=product_id, artikul_ln=product.title_ln, artikul_ru=product.title_ru
        )
        product_item_artikul.append(product_item.artikul_ln)

    push_to_moysklad(product_item_artikul, product)


@shared_task()
def mass_create_cart(carts: list, user_id: int):
    with transaction.atomic():
        for cart in carts:
            user_cart, _ = Cart.objects.get_or_create(
                product_id=cart['id'], user_id=user_id, is_deleted=False, is_active=True
            )
            price = get_active_product_item_sell_price().filter(product_item_id=cart['id']).first()
            if price:
                user_cart.price = price.price
            user_cart.quantity += cart['quantity']
            user_cart.save()

    # params = [
    #     (int(cart['id']), int(cart['quantity']), user_id, 'now()', 'now()', False, True)
    #     for cart in carts
    # ]
    # query = """
    #     INSERT INTO
    #         product_cart (product_id, quantity, user_id, created_at, update_at, is_deleted, is_active)
    #     VALUES {}""".format(",".join(map(str, params)))
    # with connection.cursor() as cursor:
    #     cursor.execute(query)


@shared_task()
def mass_delete_carts(carts_id, user_id):
    carts_id = str(carts_id).replace('[', '(').replace(']', ')')
    query = """
        UPDATE 
            product_cart
        SET
            is_deleted = true, is_active = false
        WHERE
            user_id = %s AND id IN %s
    """%(user_id, carts_id)
    with connection.cursor() as cursor:
        cursor.execute(query)
