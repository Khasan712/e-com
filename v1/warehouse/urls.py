from django.urls import path
from .views import (
    ImportToWarehouseCartApi,
    ImportToWarehouseApi
)


urlpatterns = [
    path("import/", ImportToWarehouseApi.as_view()),
    path("import-cart/", ImportToWarehouseCartApi.as_view()),
]

