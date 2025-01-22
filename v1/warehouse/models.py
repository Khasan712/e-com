from django.db import models
from v1.product.models import (
    ProductItem,
    Product,
    Characteristic,
)
from v1.utilis.abstract_classes.abstract_classes import AbstractDefaultClass
from v1.user.models import Seller


class Warehouse(AbstractDefaultClass):
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self) -> str:
        return self.title


class ImportToWarehouseCart(AbstractDefaultClass):
    warehouse = models.ForeignKey(Warehouse, on_delete=models.SET_NULL, null=True)
    seller = models.ForeignKey(Seller, on_delete=models.SET_NULL, null=True)


class ImportProductToWarehouse(AbstractDefaultClass):
    import_to_warehouse_cart = models.ForeignKey(ImportToWarehouseCart, on_delete=models.SET_NULL, null=True)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)

    # def __str__(self) -> str:
    #     return self.product.title_ln


class ProductInWarehouse(AbstractDefaultClass):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    warehouse = models.ForeignKey(Warehouse, on_delete=models.SET_NULL, null=True)
    seller = models.ForeignKey(Seller, on_delete=models.SET_NULL, null=True)
    
    def __str__(self) -> str:
        return self.product.title_ln


class ImportPriceProductInWarehouse(AbstractDefaultClass):
    import_product_to_warehouse = models.ForeignKey(ImportProductToWarehouse, on_delete=models.SET_NULL, null=True)
    product_in_warehouse = models.ForeignKey(ProductInWarehouse, on_delete=models.SET_NULL, null=True)
    linked_characteristic = models.ForeignKey(ProductItem, on_delete=models.SET_NULL, null=True, blank=True)
    import_price = models.PositiveIntegerField(default=0)


class SellPriceProductInWarehouse(AbstractDefaultClass):
    product_in_warehouse = models.ForeignKey(ProductInWarehouse, on_delete=models.SET_NULL, null=True)
    linked_characteristic = models.ForeignKey(ProductItem, on_delete=models.SET_NULL, null=True, blank=True)
    price = models.PositiveIntegerField(default=0)


class ImportQuantityProductInWarehouse(AbstractDefaultClass):
    import_product_to_warehouse = models.ForeignKey(ImportProductToWarehouse, on_delete=models.SET_NULL, null=True)
    product_in_warehouse = models.ForeignKey(ProductInWarehouse, on_delete=models.SET_NULL, null=True)
    linked_characteristic = models.ForeignKey(ProductItem, on_delete=models.SET_NULL, null=True, blank=True)
    quantity = models.PositiveBigIntegerField(default=0)

    def __str__(self) -> str:
        return f"{self.product_in_warehouse.product.title_ln}, qty: {self.quantity}"


class QuantityProductInWarehouse(AbstractDefaultClass):
    product_in_warehouse = models.ForeignKey(ProductInWarehouse, on_delete=models.SET_NULL, null=True)
    linked_characteristic = models.ForeignKey(ProductItem, on_delete=models.SET_NULL, null=True, blank=True)
    quantity = models.PositiveBigIntegerField(default=0)

    def __str__(self) -> str:
        return f"qty: {self.quantity}"


