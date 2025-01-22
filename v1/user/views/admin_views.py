from rest_framework_simplejwt.views import TokenObtainPairView
from v1.user.serializers.admin_serializers import MyTokenObtainPairSerializer, SellerSerializer, ClientGetSerializer
from v1.utilis.mixins.generic_mixins import CustomListAPIView, CustomUpdateAPIView, CustomRetrieveAPIView
from v1.utilis.querysets.get_active_querysets import get_active_sellers, get_active_not_confirmed_clients


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


class SellerApi(CustomListAPIView):
    queryset = get_active_sellers()
    serializer_class = SellerSerializer


class ClientListAPI(CustomListAPIView):
    serializer_class = ClientGetSerializer
    queryset = get_active_not_confirmed_clients()


class ClientConfirmAPI(CustomUpdateAPIView, CustomRetrieveAPIView):
    serializer_class = ClientGetSerializer
    queryset = get_active_not_confirmed_clients()
