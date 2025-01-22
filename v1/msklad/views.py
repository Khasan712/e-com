from rest_framework.views import APIView
from rest_framework.response import Response


class OrderDeleteApi(APIView):
    """
    update product quantity in warehouse.
    """

    def post(self, request, *args, **kwargs):
        return Response(status=200)


class ProductDeleteApi(APIView):
    """
    update product quantity in warehouse.
    """

    def post(self, request, *args, **kwargs):
        return Response(status=200)


class QuantityUpdateApi(APIView):
    """
    update product quantity in warehouse.
    """

    def post(self, request, *args, **kwargs):
        return Response(status=200)


class OrderStatusUpdateApi(APIView):
    """
    Update order status
    """

    def post(self, request, *args, **kwargs):
        return Response(status=200)


class ProductUpdateApi(APIView):
    """
    Update product
    """

    def post(self, request, *args, **kwargs):
        return Response(status=200)

