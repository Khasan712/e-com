from rest_framework import serializers
from rest_framework.validators import ValidationError

from v1.order.models import Order, OrderItem
from v1.order.tasks import push_orders_to_moysklad_task_and_save
from v1.utilis.querysets.get_active_querysets import get_active_cart


class OrderItemListSerializer(serializers.ModelSerializer):
    created_at = serializers.SerializerMethodField()
    status = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()

    class Meta:
        model = OrderItem
        fields = ('id', 'quantity', 'price', 'product', 'status', 'created_at', 'image')

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


class OrderListSerializer(serializers.ModelSerializer):
    items = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = ('id', 'created_at', 'status', 'items')

    def get_items(self, instance):
        return OrderItemsSerializer(instance.order_items.filter(is_deleted=False, is_active=True), many=True).data


class OrderSerializer(serializers.Serializer):
    carts = serializers.ListField(write_only=True, required=True)

    def validate(self, attrs):
        res = super().validate(attrs)
        carts = res['carts']
        user_id = self.context['user_id']
        carts_obj = get_active_cart().filter(id__in=carts, user_id=user_id, product__moy_sklad_id__isnull=False)
        if carts_obj.count() != len(carts):
            raise ValidationError("Cart does not exist or moy sklad id not found!")
        return res

    def create(self, validated_data):
        push_orders_to_moysklad_task_and_save(
            validated_data['carts'], user_id=self.context['user_id']
        )
        return validated_data
