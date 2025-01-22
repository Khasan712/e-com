from rest_framework_simplejwt.views import TokenObtainPairView
from v1.user.serializers.api_serializers import (
    ClientTokenObtainPairSerializer,
)
from rest_framework.decorators import api_view
from django.db import connection
from rest_framework.response import Response
from django.http import JsonResponse
import json, ujson
from v1.user.models import User


@api_view(['GET'])
def get_users(request):

    with connection.cursor() as cursor:
        cursor.execute("SELECT get_users()")
        result = cursor.fetchone()[0]
    return Response({"data": ujson.loads(result)})

    # users = User.objects.values("id", "phone_number")
    # return Response({"data": users})


class ClientTokenObtainPairView(TokenObtainPairView):
    serializer_class = ClientTokenObtainPairSerializer



