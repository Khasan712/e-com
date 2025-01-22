from django.urls import path
from v1.msklad.views import (
    QuantityUpdateApi, ProductUpdateApi, OrderStatusUpdateApi, OrderDeleteApi,
    ProductDeleteApi
)


urlpatterns = [
    path("order-delete/", OrderDeleteApi.as_view()),
    path("product-delete/", ProductDeleteApi.as_view()),
    path("quantity-update/", QuantityUpdateApi.as_view()),
    path("product-update/", ProductUpdateApi.as_view()),
    path("order-status-update/", OrderStatusUpdateApi.as_view())
]
