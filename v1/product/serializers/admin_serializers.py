from django.db import transaction
from rest_framework import serializers
from v1.product.models import AdsProductItem, MainBanner, TopCategory, TopProductItem
from v1.product.models import (
    Barcode, Brand, Category, CharacterItem, Country, Ikpu, Model,
    Product, ProductItem, ProductItemSellPrice, Sku
)
from v1.product.tasks import product_task
from v1.services.moysklad.update_product_item import update_product_item
from v1.utilis.querysets.get_active_querysets import (
    get_active_barcode, get_active_characteristics, get_active_ikpu, get_active_product_item_sell_price,
    get_active_product_items, get_active_product_queryset, get_active_sku

)


class AdsProductItemSerialzier(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    class Meta:
        model = AdsProductItem
        fields = ("id", "product_item", "image")

    def get_image(self, obj):
        if len(obj.product_item.images) > 0:
            return obj.product_item.images[-1]['url']
        return obj.product_item.product.images[-1]['url'] if len(obj.product_item.product.images) > 0 else None

    def to_representation(self, instance):
        res = super().to_representation(instance)
        res['product_item'] = {
            "artikul_ln": instance.product_item.product.title_ln,
            "artikul_ru": instance.product_item.product.title_ru,
            "price": instance.product_item.get_price,
        }
        return res


class ProductItemsApiSerializer(serializers.ModelSerializer):
    price = serializers.SerializerMethodField()

    class Meta:
        model = ProductItem
        fields = ("id", "artikul_ln", "artikul_ru", "price")

    def get_price(self, obj):
        return obj.get_price


class MainBannerSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    class Meta:
        model = MainBanner
        fields = ("id", "url", "title_ln", "title_ru", "description_ln", "description_ru", "image")

    def get_image(self, obj):
        return obj.images[-1]['url'] if len(obj.images) > 0 else None


class ProductItemUpdateSerialzier(serializers.Serializer):
    sku = serializers.CharField(max_length=7)
    items = serializers.ListField()

    def create(self, validated_data):
        pk = self.context['pk']
        sku = validated_data['sku']
        items = validated_data['items']
        try:
            product_card = get_active_product_queryset().get(id=pk)
        except:
            raise serializers.ValidationError("Product does not exist.")
        with transaction.atomic():
            exists_sku = get_active_sku().filter(seller_id=product_card.seller.id, product_id=product_card.id).first()
            if not exists_sku:
                seller_sku = get_active_sku().filter(seller_id=product_card.seller.id, sku=sku).first()
                if seller_sku:
                    raise serializers.ValidationError("Given sku is already in use.")
                Sku.objects.create(seller_id=product_card.seller.id, product_id=product_card.id, sku=sku)
            
            for item in items:

                """ Checking product item """
                product_item = get_active_product_items().filter(
                    id=item['id'], product_id=product_card.id
                ).first()
                if not product_item:
                    raise serializers.ValidationError(f"Product item not found! id: {item['id']}")
                
                """ Conf Ikpu """
                if not item.get("ikpu") and not product_item.ikpu:
                    raise serializers.ValidationError("ikpu not given")
                if item.get("ikpu"):
                    ikpu = get_active_ikpu().filter(id=item['ikpu']).first()
                    if not ikpu:
                        raise serializers.ValidationError("Ikpu not found.")
                    product_item.ikpu = ikpu

                """ Conf barcode """
                if not product_item.barcode:
                    barcode = item.get("barcode")
                    if not barcode:
                        barcode = Barcode.objects.generate_barcode()
                    else:
                        barcode = get_active_barcode().get(id=barcode)
                    product_item.barcode = barcode
                product_item.save()

                """ Giving selling price """
                product_item_sell_price = get_active_product_item_sell_price().filter(
                    product_item_id=item['id']
                ).first()
                if not item.get("price") and not product_item_sell_price:
                    raise serializers.ValidationError(f"There is not selling price in this product item {item['id']}")
                if item.get("price"):
                    if product_item_sell_price:
                        product_item_sell_price.is_active = False
                        product_item_sell_price.save()
                    ProductItemSellPrice.objects.create(
                        product_item_id=item['id'], price=item['price']
                    )
                    product = {
                        'price': item['price'],
                        'moy_sklad_id': product_item.moy_sklad_id
                    }
                    # moy sklad update price
                    update_product_item(product)
        return validated_data


class CategoryCreateSerialzier(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ("id", 'title_ln', 'title_ru', 'parent')
    

class CategoryRetrieveSerialzer(serializers.ModelSerializer):
    children = serializers.SerializerMethodField()
    title = serializers.CharField(allow_blank=True, default='')

    def __init__(self, *args, **kwargs):
        context = kwargs.pop('context', {})
        super().__init__(*args, **kwargs)
        self.context.update(context)

    class Meta:
        model = Category
        fields = ("id", 'icon', 'title', 'children')

    def get_children(self, obj):
        serializer = self.__class__(obj.children.all(), many=True, context=self.context)
        return serializer.data

    def to_representation(self, instance):
        res = super().to_representation(instance)
        lang = self.context['lang']
        role = self.context.get('role')
        if role == 'admin':
            res['title'] = {
                'title_ln': instance.title_ln,
                'title_ru': instance.title_ru,
            }
            return res
        else:
            language_fields = {
                'uz-LN': ('title_ln',),
                'ru-RU': ('title_ru',),
            }
            title_field = language_fields.get(lang, ('title',))
            res['title'] = getattr(instance, title_field[0], None)
            return res


class CategoryChildrenSerialzer(serializers.ModelSerializer):
    title = serializers.CharField(allow_blank=True, default='')
    children = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ("id", 'icon', 'title', "children")

    def get_children(self, instance):
        return True if instance.children.exists() else None


class ProductCreateSerializer(serializers.ModelSerializer):
    """
    Product create serializer by admin
    """
    characteristics = serializers.ListField(required=False, write_only=True)
    images = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = (
            'seller', 'category', 'country', 'brand', 'model',
            'title_ln', 'title_ru', 'description_ln', 'description_ru',
            'attributes_ln', 'attributes_ru', 'composition_ln', 'composition_ru',
            'sertificate_ln', 'sertificate_ru', 'characteristics', 'images'
        )
        extra_kwargs = {
            "seller": {"allow_null": False, "required": True},
            "category": {"allow_null": False, "required": True},
            "title_ln": {"allow_null": False, "required": True},
            "title_ru": {"allow_null": False, "required": True},
            "description_ln": {"allow_null": False, "required": True},
            "description_ru": {"allow_null": False, "required": True},
            "characteristics": {"allow_null": True, "required": False},
        }

    def get_images(self, obj):
        if len(obj.images) > 0:
            return [image['url'] for image in obj.images]
        return None

    def create(self, validated_data):
        with transaction.atomic():
            try:
                characteristics = validated_data.pop("characteristics")
            except:
                characteristics = None

            instance = self.Meta.model(**validated_data)
            instance.save()

            product_task.delay(instance.id, characteristics)

        return instance
    
    def to_representation(self, instance):
        return {
            "id": instance.id,
        } 


class ProductItemSerialzier(serializers.ModelSerializer):
    title = serializers.SerializerMethodField()
    price = serializers.SerializerMethodField()
    ikpu = serializers.SerializerMethodField()
    
    class Meta:
        model = ProductItem
        fields = ("id", 'title', 'status', 'price', 'barcode', 'ikpu')

    def get_price(self, instance):
        price = get_active_product_item_sell_price().filter(
            product_item=instance.id
        ).first()
        return price.price if price else None
    
    def get_ikpu(self, instance):
        ikpu = instance.ikpu
        if ikpu :
            return {
                "id": instance.ikpu.id,
                "code": instance.ikpu.code,
            }
        return None

    def get_title(self, instance):
        characteristics_titles = instance.characteristics.values_list("title__title_ln", flat=True)
        return ", ".join(characteristics_titles)


class ProductGetSerializer(serializers.ModelSerializer):
    title = serializers.CharField()
    category_name = serializers.CharField()
    seller_name = serializers.CharField()
    sku = serializers.CharField()

    class Meta:
        model = Product
        fields = ('id', 'title', 'created_at', 'seller_name', 'category_name', 'sku')


class ProductDetailSerialzier(serializers.ModelSerializer):
    characteristics = serializers.SerializerMethodField()
    attributes = serializers.SerializerMethodField()
    title = serializers.SerializerMethodField()
    composition = serializers.SerializerMethodField()
    sertificate = serializers.SerializerMethodField()
    description = serializers.SerializerMethodField()
    images = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = (
            'id', 'title', 'created_at', 'seller', 'category', 'attributes', 'description',
            'characteristics', 'country', 'brand', 'model', 'composition', 'sertificate', 'images'
        )

    def get_title(self, instance):
        return {
            'ln': instance.title_ln,
            'ru': instance.title_ru,
        }
    
    def get_attributes(self, instance):
        return {
            'ln': instance.attributes_ln,
            'ru': instance.attributes_ru,
        }

    def get_composition(self, instance):
        return {
            'ln': instance.composition_ln,    
            'ru': instance.composition_ru,    
        }
    
    def get_description(self, instance):
        return {
            'ln': instance.description_ln,    
            'ru': instance.description_ru,    
        }
    
    def get_sertificate(self, instance):
        return {
            'ln': instance.sertificate_ln,
            'ru': instance.sertificate_ru,
        }

    def get_product_characteristics(self, characteristics):
        characteristic_data = []
        characteristic_ids = [characteristic.id for characteristic in characteristics]
        child_characteristics = get_active_characteristics().filter(parent_id__in=characteristic_ids)

        for characteristic in characteristics:
            child_items = self.get_product_characteristics(
                [char for char in child_characteristics if char.parent_id == characteristic.id]
            )

            characteristic_data.append({
                'id': characteristic.id,
                'title': characteristic.title.title_ln,
                'items': child_items
            })

        return characteristic_data

    def get_characteristics(self, instance):
        # return self.get_product_characteristics(instance.product_characteristics.filter(parent__isnull=True))
        root_characteristics = instance.product_characteristics.filter(parent__isnull=True)
        return self.get_product_characteristics(root_characteristics)

    def get_category_parents(self, category):
        return {
            'id': category.id,
            'title': category.title_ln,
            'parent': None if not category.parent else self.get_category_parents(category.parent)    
        }
    
    def get_images(self, instance):
        if len(instance.images) > 0:
            return [image['url'] for image in instance.images]
        return None
    
    def to_representation(self, instance):
        res = super().to_representation(instance)
        if res.get("seller"):
            res['seller'] = {
                'id': instance.seller.id,
                'first_name': instance.seller.first_name,
                'phone_number': instance.seller.phone_number,
            }

        if res.get('category'):
            res['category'] = self.get_category_parents(instance.category)

        if res.get('brand'):
            res['brand'] = {
                'id': instance.brand.id,
                'title': {
                    'ln': instance.brand.title_ln,
                    'ru': instance.brand.title_ru,
                }
            }

        if res.get('model'):
            res['model'] = {
                'id': instance.model.id,
                'title': {
                    'ln': instance.model.title_ln,
                    'ru': instance.model.title_ru,
                }
            }

        if res.get('country'):
            res['country'] = {
                'id': instance.country.id,
                'title': {
                    'ln': instance.country.title_ln,
                    'ru': instance.country.title_ru,
                }
            }

        return res


class ModelSerializer(serializers.ModelSerializer):
    title = serializers.CharField()
    
    class Meta:
        model = Model
        fields = ("id", 'title')


class CharacterItemChildrenSerializer(serializers.ModelSerializer):
    title = serializers.CharField()

    class Meta:
        model = CharacterItem
        fields = ("id", "title", "value")


class CharacterItemSerializer(serializers.ModelSerializer):
    title = serializers.CharField()
    values = serializers.SerializerMethodField()
    
    def __init__(self, instance=None, data=..., **kwargs):
        super().__init__(instance, data, **kwargs)

    class Meta:
        model = CharacterItem
        fields = ("id", "title", "value", "values")

    def get_values(self, instance, *args, **kwargs):
        items = self.context['queryset'].filter(parent_id=instance.id)
        serializer = CharacterItemChildrenSerializer(items, many=True)
        return serializer.data


class BrandSerialzier(serializers.ModelSerializer):
    title = serializers.CharField()

    class Meta:
        model = Brand
        fields = ("id", 'title')


class CountrySerialzier(serializers.ModelSerializer):
    title = serializers.CharField()

    class Meta:
        model = Country
        fields = ("id", 'title')
    

class BarcodeSerialzier(serializers.ModelSerializer):

    class Meta:
        model = Barcode
        fields = ("id", 'code', 'title')


class IkpuSerialzier(serializers.ModelSerializer):

    class Meta:
        model = Ikpu
        fields = ("id", 'code', 'title_ln', "title_ru")
    

class SkuSerialzier(serializers.ModelSerializer):

    class Meta:
        model = Sku
        fields = ("id", 'code', 'title_ln', "title_ru")


class TopCategorySerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    class Meta:
        model = TopCategory
        fields = ("id", "category", 'url', 'image')

    def get_image(self, obj):
        return obj.images[-1]['url'] if len(obj.images) > 0 else None

    def to_representation(self, instance):
        res = super().to_representation(instance)
        res['category'] = {
            'id': instance.category.id,
            'title_ln': instance.category.title_ln,
            'title_kr': instance.category.title_kr,
        }
        return res
    

class TopProductItemSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    class Meta:
        model = TopProductItem
        fields = ("id", "product_item", 'image')
    
    def get_image(self, obj):
        if len(obj.product_item.images) > 0:
            return obj.product_item.images[-1]['url']
        return obj.product_item.product.images[-1]['url'] if len(obj.product_item.product.images) > 0 else None

    def to_representation(self, instance):
        res = super().to_representation(instance)
        res['product_item'] = {
            "id": instance.product_item.id,
            "artikul_ln": instance.product_item.artikul_ln,
            "artikul_ru": instance.product_item.artikul_ru,
            "price": instance.product_item.get_price,
        }
        return res

