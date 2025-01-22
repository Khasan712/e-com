from django.contrib import admin
from .models import (
    User,
    Seller,
    Client,
    Admin
)


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("id", 'first_name', 'phone_number', 'role', 'is_active')
    # form = MyUserCreationForm
    

@admin.register(Seller)
class SellerAdmin(admin.ModelAdmin):
    list_display = ("id", 'first_name', 'phone_number', 'role', 'is_active')
        

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ("id", 'first_name', 'phone_number', 'role', 'is_active')


@admin.register(Admin)
class AdminAdmin(admin.ModelAdmin):
    list_display = ("id", 'first_name', 'phone_number', 'role', 'is_active')