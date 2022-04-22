from rest_framework.permissions import BasePermission
from rest_framework import permissions

ROLE_LIST = {'admin', 'moderator'}


class IsAdminOnly(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_staff or (request.user.is_admin)

    def has_object_permission(self, request, view, obj):
        return request.user.is_staff or (request.user.is_admin)


class AdminOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
            and (request.user.is_staff or request.user.is_admin)
        )


class WriteOnlyAuthorOr(BasePermission):
    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):

        return (request.method in permissions.SAFE_METHODS
                or (obj.author == request.user)
                or (request.user.is_authenticated
                    and (request.user.is_staff
                         or (request.user.role in ROLE_LIST))
                    )
                )
