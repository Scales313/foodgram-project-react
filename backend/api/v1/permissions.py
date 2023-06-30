from rest_framework import permissions


class IsAdminRole(permissions.BasePermission):
    message = 'Необходимы права администратора!'

    def has_permission(self, request, view):
        return (request.user.role == 'admin' or request.user.is_superuser)


class IsAuthorOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.author == request.user
