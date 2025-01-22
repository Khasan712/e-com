from django.db import transaction

from v1.msklad.services import push_orders_to_moysklad
from v1.order.models import Order, OrderItem
from v1.utilis.querysets.get_active_querysets import get_active_cart


# @shared_task()
def push_orders_to_moysklad_task_and_save(carts: list, user_id: int):
    carts = get_active_cart().filter(id__in=carts, user_id=user_id, product__moy_sklad_id__isnull=False)
    orders = push_orders_to_moysklad(carts)
    if orders:
        order = Order.objects.create(
            user_id=user_id, name=orders['name'], moy_sklad_order_id=orders['id'], json_data=orders
        )
        with transaction.atomic():
            order_items = [
                OrderItem(
                    order_id=order.id,
                    cart_id=cart.id,
                    product_id=cart.product.id,
                    quantity=cart.quantity,
                    price=cart.price,
                    product_moy_sklad_id=cart.product.moy_sklad_id
                )
                for cart in carts
            ]
            OrderItem.objects.bulk_create(order_items)
        carts.update(is_deleted=True, is_active=False)
