from rest_framework.viewsets import GenericViewSet

from v1.order.serializers.admin_serializers import OrderGetSerializer, OrderItemListSerializer
from v1.utilis.mixins.generic_mixins import CustomListModelMixin, CustomRetrieveModelMixin
from v1.utilis.querysets.get_active_querysets import get_active_orders, get_active_order_items


class OrderApi(
    CustomListModelMixin,
    CustomRetrieveModelMixin,
    GenericViewSet
):
    queryset = get_active_orders()

    def get_queryset(self):
        if self.request.method == 'GET' and not self.kwargs.get('pk'):
            return get_active_order_items()
        elif self.request.method == 'GET' and self.kwargs.get('pk'):
            return super().get_queryset()

    def get_serializer_class(self):
        if self.request.method == 'GET' and not self.kwargs.get('pk'):
            return OrderItemListSerializer
        elif self.request.method == 'GET' and self.kwargs.get('pk'):
            return OrderGetSerializer
