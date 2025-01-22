from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, AbstractUser
from v1.user.enums import UserRole
from v1.user.managers import (
    AdminManager,
    CustomManager,
    ClientManager,
    SellerManager
)


class User(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100, blank=True, null=True)
    phone_number = models.CharField(max_length=100, unique=True)
    role = models.CharField(max_length=6, choices=UserRole.choices())
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    is_confirmed = models.BooleanField(default=False)

    USERNAME_FIELD = "phone_number"
    REQUIRED_FIELDS = ["role"]

    objects = CustomManager()

    def __str__(self) -> str:
        return self.phone_number
    
class Seller(User):
    objects = SellerManager()

    class Meta:
        proxy = True

class Client(User):
    objects = ClientManager()

    class Meta:
        proxy = True



class Admin(User):
    objects = AdminManager()

    class Meta:
        proxy = True