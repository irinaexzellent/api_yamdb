from rest_framework.permissions import BasePermission
from rest_framework import permissions


class IsAdminOnly(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_staff or (request.user.role == 'admin')

    def has_object_permission(self, request, view, obj):
        return request.user.is_staff or (request.user.role == 'admin')


class AdminOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
            and (request.user.is_staff or request.user.role == "admin")
        )

