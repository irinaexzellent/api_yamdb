from rest_framework.permissions import BasePermission


class IsAdminOnly(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_staff or (request.user.role == 'admin')
