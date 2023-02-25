from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.user==request.user
class IsAdminOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj ):
        if request.method in permissions.SAFE_METHODS:
            return True
        return bool(request.user and request.user.is_staff)
class AnonPermissionOnly(permissions.BasePermission):
    message='You are already authenticated'
    def has_permission(self, request, view):
        return not request.user.is_authenticated
