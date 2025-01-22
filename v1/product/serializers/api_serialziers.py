from rest_framework import serializers
from v1.product.models import (
    Brand, MainBanner, Model, Product, TopCategory, TopProductItem, Cart
)
from v1.services.full_filter import category_children_tree
from v1.utilis.querysets.get_active_querysets import get_active_characteristics


class CartDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = ('id', 'quantity')


class ClientBrandSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Brand
        fields = ("id", 'title_ln', "title_ru")


class ClientModelSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Model
        fields = ("id", 'title_ln', "title_ru")


class GetProductDetailSerializer(serializers.ModelSerializer):
    images = serializers.SerializerMethodField()
    characteristics = serializers.SerializerMethodField()
    items = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = (
            "title_ln", "title_ru", "seller", "brand", "model", "category", "images", "characteristics",
            "items", "attributes_ln", "attributes_ru", "composition_ln", "composition_ru",
            "sertificate_ln", "sertificate_ru"
        )

    def get_items(self, instance):
        # items = instance.product_item
        pass

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

    def get_characteristics(self, obj):
        parent_characteristics = obj.product_characteristics.filter(parent__isnull=True)
        return self.get_product_characteristics(parent_characteristics)
    
    def get_images(self, obj):
        if len(obj.images) > 0:
            return [
                image['url']
                for image in obj.images    
            ]
        return None
    
    def to_representation(self, instance):
        res = super().to_representation(instance)
        if res.get("seller"):
            res['seller'] = {
                "first_name": instance.seller.first_name,
                "last_name": instance.seller.last_name
            }
        if res.get("brand"):
            res['brand'] = {
                "title_ln": instance.brand.title_ln,
                "title_ru": instance.brand.title_ru
            }
        if res.get("model"):
            res['model'] = {
                "title_ln": instance.model.title_ln,
                "title_ru": instance.model.title_ru
            }
        if res.get("category"):
            res['category'] = category_children_tree(instance.category)
        return res


class GetProductItemSerializer(serializers.Serializer):
    image = serializers.SerializerMethodField()

    def get_image(self, instance):
        if len(instance.images) > 0:
            return instance.images[0]['url']
        return instance.product.images[0]['url'] if len(instance.product.images) > 0 else None
    
    def to_representation(self, instance):
        res = super().to_representation(instance)
        res['id'] = instance.id
        res['title_ln'] = "{}".format(instance.product.title_ln)
        res['title_ru'] = "{}".format(instance.product.title_ru)
        res['price'] = "{}".format(instance.price)
        return res


class NewProductsSerializer(serializers.Serializer):
    id = serializers.SerializerMethodField()
    product_item = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()

    def get_product_last_item(self, obj):
        return obj.product_card.last()
    
    def get_id(self, obj):
        return obj.id

    def get_product_item(self, obj):
        return {
            "id": self.get_product_last_item(obj).id,
            "artikul_ln": obj.title_ln,
            "artikul_ru": obj.title_ru,
            "price": self.get_product_last_item(obj).get_price,
        }

    def get_image(self, obj):
        product_item = self.get_product_last_item(obj)
        if len(product_item.images) > 0:
            return product_item.images[0]['url']
        return obj.images[0]['url'] if len(obj.images) > 0 else None


class ClientMainBannerSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    class Meta:
        model = MainBanner
        fields = ("id", "url", "title_ln", "title_ru", "description_ln", "description_ru", "image")

    def get_image(self, obj):
        try:
            return obj.images[-1]['url']
        except:
            return None
    

class ClientTopProductItemSerializer(serializers.ModelSerializer):
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
            "artikul_ln": instance.product_item.product.title_ln,
            "title_ru": instance.product_item.product.title_ru,
            "price": instance.product_item.get_price,
        }
        return res


class ClientTopCategorySerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    class Meta:
        model = TopCategory
        fields = ("id", "category", 'url', 'image')

    def get_image(self, obj):
        try:
            return obj.images[-1]['url']
        except:
            return None

    def to_representation(self, instance):
        res = super().to_representation(instance)
        res['category'] = {
            'id': instance.category.id,
            'title_ln': instance.category.title_ln,
            'title_kr': instance.category.title_kr,
        }
        return res
