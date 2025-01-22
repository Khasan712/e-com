from django.contrib.auth.models import AnonymousUser
from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsAdmin(BasePermission):
    message = "You must be the admin of this website"

    def has_permission(self, request, view):
        if not isinstance(request.user, AnonymousUser):
            # if request.method in SAFE_METHODS:
            return bool(request.user.role == "admin")
        