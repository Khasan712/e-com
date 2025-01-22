from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from v1.user.models import Seller, Client


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    Custom obtain serializer for adding user role
    """
    def validate(self, attrs):
        data = super().validate(attrs)
        user = self.user
        if user.role != 'admin':
            raise serializers.ValidationError("Admin not found")
        data['role'] = user.role
        return data
    

class SellerSerializer(serializers.ModelSerializer):
    """
    Seller serializer for method GET
    """
    class Meta:
        model = Seller
        fields = ("id", "first_name", 'last_name', 'phone_number')


class ClientGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ("id", "first_name", 'last_name', 'phone_number', "is_confirmed")
    

class ClientSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(max_length=15)
    password2 = serializers.CharField(max_length=15)

    class Meta:
        model = Client
        fields = ("id", "first_name", 'last_name', 'phone_number', "password1", "password2")

        extra_kwargs = {
            'first_name': {"allow_blank": False, "required": True},
            'last_name': {"allow_blank": False, "required": True},
        }

    def validate(self, attrs):

        if attrs.get('password1') != attrs.get('password2'):
            raise serializers.ValidationError("Error: Passwords not same. ")
        password = attrs.pop("password1")
        attrs.pop("password2")
        attrs['password'] = password
        return attrs

    def create(self, validated_data):
        password = validated_data['password']
        client = Client.objects.create_user(
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            phone_number=validated_data['phone_number'],
            role='client',
            password=password
        )
        setattr(client, 'password1', validated_data.get("password1"))
        setattr(client, 'password2', validated_data.get("password2"))
        return client

