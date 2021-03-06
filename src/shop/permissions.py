from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    message = "You do not have permission to create, update or delete shop for other users."

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.user == request.user
