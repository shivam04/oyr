from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    message = "You do not have permission to view or update other users data."

    def has_object_permission(self, request, view, obj):
        if hasattr(obj, "user"):
            return obj.user == request.user
        return obj == request.user


class DeletePermission(permissions.BasePermission):
    message = "You do not have permission to delete data."

    def has_permission(self, request, view):
        return bool(
            request.user and
            (request.user.is_staff or request.user.is_authenticated)
        )

