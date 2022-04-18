from rest_framework.permissions import BasePermission
from rest_framework import permissions


class IsAdminOnly(BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
            and request.user.role == "admin"
        )
