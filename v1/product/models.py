from django.db import models
from v1.product.managers import BarcodeCustomManager
from v1.utilis.abstract_classes.abstract_classes import (
    AbstractBaseClass,
    AbstractBaseTitleClass,
    AbstractDefaultClass
)
from v1.user.models import Seller
from v1.utilis.enums import ProductItemStatus


class Cart(AbstractDefaultClass):
    product = models.ForeignKey("product.ProductItem", on_delete=models.CASCADE)
    price = models.FloatField(default=0)
    quantity = models.PositiveIntegerField(default=0)
    user = models.ForeignKey("user.User", on_delete=models.CASCADE)


class QuestionInProductDetail(AbstractDefaultClass):
    product_item = models.ForeignKey('product.ProductItem', on_delete=models.CASCADE)
    user = models.ForeignKey('user.User', on_delete=models.CASCADE, blank=True, null=True)
    first_name = models.CharField(max_length=255, blank=True, null=True)
    is_active = models.BooleanField(default=False)
    

class MainBanner(AbstractBaseClass):
    url = models.CharField(max_length=255)
    images = models.JSONField(default=list)

    def __str__(self) -> str:
        return self.title_ln


class Category(AbstractBaseClass):
    """
    Product Category
    """
    icon = models.ImageField(upload_to='product/category/icons/', blank=True, null=True)
    parent = models.ForeignKey(
        'self', on_delete=models.SET_NULL, blank=True, null=True, related_name='children'
    )

    def __str__(self) -> str:
        return f"{self.id} - {self.title_ln}"

    class Meta:
        verbose_name_plural = "3) Categories"


class Brand(AbstractBaseTitleClass):
    """
    Product Brand
    """
    pass


class Model(AbstractBaseTitleClass):
    brand = models.ForeignKey(Brand, on_delete=models.SET_NULL, null=True)


class Country(AbstractBaseTitleClass):
    """
    Country for know Where product made or came
    """
    pass


class Barcode(AbstractDefaultClass):
    code = models.PositiveBigIntegerField(unique=True)
    title = models.CharField(max_length=255, blank=True, null=True)

    objects = BarcodeCustomManager()
    
    def __str__(self) -> str:
        return f"{self.code} {self.title}"


class Ikpu(AbstractBaseTitleClass):
    code = models.CharField(max_length=255, blank=True, null=True)
    group = models.CharField(max_length=800, blank=True, null=True)
    class_group = models.CharField(max_length=800, blank=True, null=True)
    position = models.CharField(max_length=800, blank=True, null=True)
    sub_position = models.CharField(max_length=800, blank=True, null=True)
    brand = models.CharField(max_length=800, blank=True, null=True)

    def __str__(self) -> str:
        return f"{self.title_ln} {self.code}"


class Product(AbstractBaseClass):
    """
    Product model
    """
    seller = models.ForeignKey(Seller, on_delete=models.SET_NULL, null=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name="product_category")
    brand = models.ForeignKey(Brand, on_delete=models.SET_NULL, blank=True, null=True)
    model = models.ForeignKey(Model, on_delete=models.SET_NULL, blank=True, null=True)
    country = models.ForeignKey(Country, on_delete=models.SET_NULL, blank=True, null=True)
    attributes_ln = models.JSONField(blank=True, null=True, default=dict)
    attributes_kr = models.JSONField(blank=True, null=True, default=dict)
    attributes_ru = models.JSONField(blank=True, null=True, default=dict)
    attributes_en = models.JSONField(blank=True, null=True, default=dict)

    composition_ln = models.TextField(blank=True, null=True)
    composition_ru = models.TextField(blank=True, null=True)

    sertificate_ln = models.TextField(blank=True, null=True)
    sertificate_ru = models.TextField(blank=True, null=True)

    images = models.JSONField(default=list, blank=True, null=True)

    def __str__(self) -> str:
        return f"{self.id} - {self.title_ln}"
    
    def save(self, *args, **kwargs):
        if not self.title_ru:
            self.title_ru = F'{self.title_ln} RU'
        super().save(*args, **kwargs)

    class Meta:
        verbose_name_plural = "1) Products"


class Sku(AbstractDefaultClass):
    seller = models.ForeignKey(Seller, on_delete=models.SET_NULL, null=True)
    sku = models.CharField(max_length=7)
    product = models.OneToOneField(Product, on_delete=models.SET_NULL, null=True, related_name='product_sku')

    def __str__(self) -> str:
        return f"{self.seller.phone_number} {self.sku} {self.product}"
    
    class Meta:
        unique_together = ("seller", "sku")
    

class CharacterItem(AbstractBaseTitleClass):
    """
    Product character item, for example colors, sizes, memory options
    """
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, blank=True, null=True)
    value = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.title_ln
    
    def save(self, *args, **kwargs):
        if not self.title_ru:
            self.title_ru = self.title_ln 
        super().save(*args, **kwargs)


class Characteristic(AbstractDefaultClass):
    """
    Attach character to product
    """
    title = models.ForeignKey(CharacterItem, on_delete=models.SET_NULL, null=True, related_name="characteristic_items")
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, related_name='product_characteristics')
    parent = models.ForeignKey(
        'self', on_delete=models.SET_NULL, null=True, blank=True, related_name='parent_characteristic'
    )

    def __str__(self) -> str:
        return f"{self.title.title_ln}"


class ProductItem(AbstractDefaultClass):
    """
    Connect two characteristic object for giving price, quantity we will use it
    in warehouse or selleing time to know which character of product is changing
    """
    artikul_ln = models.CharField(max_length=255, blank=True, null=True)
    artikul_ru = models.CharField(max_length=255, blank=True, null=True)
    status = models.CharField(
        max_length=12, choices=ProductItemStatus.choices(), default=ProductItemStatus.choices()[1][0]
    )
    product = models.ForeignKey(
        Product, on_delete=models.SET_NULL, null=True, related_name="product_card"
    )
    # barcode = models.ForeignKey(Barcode, on_delete=models.SET_NULL, blank=True, null=True)
    barcode = models.CharField(max_length=13, blank=True, null=True)
    ikpu = models.ForeignKey(Ikpu, on_delete=models.SET_NULL, blank=True, null=True)
    characteristics = models.ManyToManyField(Characteristic, blank=True, related_name="product_item_characteristics")
    moy_sklad_id = models.CharField(max_length=255, blank=True, null=True)
    images = models.JSONField(default=list, blank=True, null=True)
    json_data = models.JSONField(default=dict, blank=True, null=True)
    remainder = models.FloatField(default=0)
    # def __str__(self):
    #     return f"ID: {self.id} Product: {self.product.title_ln}"

    @property
    def get_price(self):
        price = self.product_item_price.select_related('product_item').filter(
            product_item_id=self.id, is_active=True, is_deleted=False
        ).last()
        return price.price if price else None
    
    class Meta:
        verbose_name_plural = "2) Product Items"
    

class ProductItemSellPrice(AbstractDefaultClass):
    product_item = models.ForeignKey(
        ProductItem, on_delete=models.SET_NULL, null=True, related_name='product_item_price'
    )
    price = models.FloatField()

    def __str__(self) -> str:
        return f"{self.price}- ID: {self.id}"


class ProductItemDiscountPrice(AbstractDefaultClass):
    product_item = models.ForeignKey(ProductItem, on_delete=models.SET_NULL, null=True)
    price = models.FloatField()

    def __str__(self) -> str:
        return f"{self.price}- ID: {self.id}"


class ProductItemImage(AbstractDefaultClass):
    """
    Product item Image
    """
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    characteristic = models.ForeignKey(ProductItem, on_delete=models.SET_NULL, null=True)
    image = models.ImageField(upload_to='product/images/')

    def __str__(self) -> str:
        return self.product.title_ln


class TopProductItem(AbstractDefaultClass):
    product_item = models.ForeignKey(ProductItem, on_delete=models.SET_NULL, null=True)
    order_num = models.IntegerField(default=0)

    # def __str__(self):
    #     return self.product_item.title_ln
    
    class Meta:
        verbose_name_plural = "4) Top Product Items"


class TopCategory(AbstractDefaultClass):
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    url = models.CharField(max_length=255, blank=True, null=True)
    images = models.JSONField(default=list, blank=True, null=True)

    def __str__(self):
        return f"{self.id}"


class AdsProductItem(AbstractDefaultClass):
    product_item = models.ForeignKey(ProductItem, on_delete=models.CASCADE, related_name="ads_product_item")
    order_num = models.PositiveIntegerField(default=1)

