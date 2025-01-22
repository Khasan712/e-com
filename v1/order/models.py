from django.db import models

from v1.utilis.abstract_classes.abstract_classes import AbstractDefaultClass
from v1.utilis.enums import OrderStatus


class Order(AbstractDefaultClass):
    user = models.ForeignKey("user.User", on_delete=models.CASCADE)
    status = models.CharField(max_length=8, choices=OrderStatus.choices(), default=OrderStatus.choices()[0][0])
    name = models.CharField(max_length=255, unique=True)
    moy_sklad_order_id = models.CharField(max_length=255)
    json_data = models.JSONField(default=dict)


class OrderItem(AbstractDefaultClass):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_items')
    cart = models.ForeignKey('product.Cart', on_delete=models.CASCADE)
    product = models.ForeignKey('product.ProductItem', on_delete=models.CASCADE)
    quantity = models.FloatField(default=0)
    price = models.FloatField(default=0)
    product_moy_sklad_id = models.CharField(max_length=255, blank=True, null=True)
    json_data = models.JSONField(default=dict)


