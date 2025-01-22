from rest_framework.viewsets import GenericViewSet

from v1.order.serializers.api_serializers import OrderSerializer, OrderListSerializer, OrderItemListSerializer
from v1.user.permissions import IsClientAuthenticated
from v1.utilis.mixins.generic_mixins import CustomCreateModelMixin, CustomListModelMixin
from v1.utilis.querysets.get_active_querysets import get_active_orders, get_active_order_items


class OrderApi(
    CustomCreateModelMixin,
    CustomListModelMixin,
    GenericViewSet
):
    permission_classes = (IsClientAuthenticated,)
    queryset = get_active_orders()

    def get_queryset(self):
        if self.request.method == 'POST':
            return super().get_queryset()
        elif self.request.method == 'GET' and not self.kwargs.get('pk'):
            queryset = get_active_order_items().filter(order__user_id=self.request.user.id)
            return queryset

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return OrderSerializer
        elif self.request.method == 'GET' and not self.kwargs.get('pk'):
            return OrderItemListSerializer
        elif self.request.method == 'GET' and self.kwargs.get('pk'):
            return OrderListSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['user_id'] = self.request.user.id
        return context


