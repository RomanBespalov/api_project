from rest_framework import permissions
from rest_framework.permissions import SAFE_METHODS, BasePermission

from reviews.models import USER_ROLE, MODERATOR_ROLE


class AdminAndSuperUser(permissions.BasePermission):
    """Админ или суперюзер"""

    def has_permission(self, request, view):
        if request.user.is_anonymous:
            return False

        return request.user.is_admin or request.user.is_superuser

    def has_object_permission(self, request, view, obj):
        return request.user.is_superuser or request.user.is_admin


class AdminOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_anonymous:
            if (request.user.role == USER_ROLE
               or request.user.role == MODERATOR_ROLE):
                return False
        return (
            request.method in SAFE_METHODS
            or request.user.is_authenticated and request.user.is_admin
        )

    def has_object_permission(self, request, view, obj):
        return (
            request.method in SAFE_METHODS
            or request.user.is_authenticated and request.user.is_admin
        )


class AuthorAdminModeratorOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        return request.method in SAFE_METHODS or request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        return (
            request.method in SAFE_METHODS
            or request.user.is_admin
            or request.user.is_moderator
            or obj.author == request.user
        )


class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_admin
