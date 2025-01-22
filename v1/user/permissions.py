from rest_framework.permissions import BasePermission


class IsClientAuthenticated(BasePermission):
    message = "You do not have access to perform this action. You have to register as a client."

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.role == 'client')