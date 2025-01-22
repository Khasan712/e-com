from rest_framework import serializers

from v1.order.models import Order, OrderItem


class OrderItemListSerializer(serializers.ModelSerializer):
    created_at = serializers.SerializerMethodField()
    status = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()
    user = serializers.SerializerMethodField()

    class Meta:
        model = OrderItem
        fields = ('id', 'quantity', 'price', 'product', 'status', 'created_at', 'image', 'user')

    def get_user(self, obj):
        return {
            'id': obj.order.user.id,
            'first_name': obj.order.user.first_name,
            'last_name': obj.order.user.last_name,
            'phone': obj.order.user.phone_number,
        }

    def get_image(self, obj):
        if len(obj.product.images) > 0:
            return obj.product.images[0]['url']
        return obj.product.product.images[0]['url'] if len(obj.product.product.images) > 0 else None

    def get_status(self, obj):
        return obj.order.status

    def get_created_at(self, obj):
        return obj.created_at

    def to_representation(self, instance):
        res = super().to_representation(instance)
        res['product'] = {
            'id': instance.product.id,
            'title_ln': instance.product.product.title_ln,
            'title_ru': instance.product.product.title_ru,
        }
        return res


class OrderItemsSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ('id', 'quantity', 'price', 'product')

    def to_representation(self, instance):
        res = super().to_representation(instance)
        res['product'] = {
            'id': instance.product.id,
            'title_ln': instance.product.product.title_ln,
            'title_ru': instance.product.product.title_ru,
        }
        return res


class OrderGetSerializer(serializers.ModelSerializer):
    items = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = ('id', 'created_at', 'status', 'items')

    def get_items(self, instance):
        return OrderItemsSerializer(instance.order_items.filter(is_deleted=False, is_active=True), many=True).data

