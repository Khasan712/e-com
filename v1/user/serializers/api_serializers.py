from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class ClientTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    Custom obtain serializer
    """
    def validate(self, attrs):
        data = super().validate(attrs)
        user = self.user
        if user.role != 'client' or not user.is_confirmed:
            raise serializers.ValidationError({"error": "Client not found or Account not verified!"})
        data['first_name'] = user.first_name
        data['last_name'] = user.last_name
        data['phone_number'] = user.phone_number
        return data


