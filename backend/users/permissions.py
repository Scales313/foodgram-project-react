from rest_framework import permissions


class IsAdminRole(permissions.BasePermission):
    message = 'Необходимы права администратора!'

    def has_permission(self, request, view):
        return (request.user.role == 'admin' or request.user.is_superuser)
