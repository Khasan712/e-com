from rest_framework.views import APIView

from v1.utilis.custom_responses import (
    serializer_error_response,
    success_response
)
from v1.utilis.permissions import (
    IsAdmin,
)
from v1.utilis.mixins.generic_mixins import (
    CustomCreateAPIView,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView
from v1.warehouse.serializers import (
    ImportToWarehouseCartSerialzier,
    ImportToWarehouseSerializer
)


class ImportToWarehouseApi(CustomCreateAPIView):
    permission_classes = (IsAuthenticated, IsAdmin)
    serializer_class = ImportToWarehouseSerializer


class ImportToWarehouseCartApi(CustomCreateAPIView):
    permission_classes = (IsAuthenticated, IsAdmin)
    serializer_class = ImportToWarehouseCartSerialzier

