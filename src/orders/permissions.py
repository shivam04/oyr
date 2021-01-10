from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    message = "You do not have permission to create, update or delete orders for other users."

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user


class IsShopOwner(permissions.BasePermission):
    message = "You do not have permission to update or delete other shop owners orders."

    def has_object_permission(self, request, view, obj):
        return request.user == obj.shop.user


class IsOrderOwner(permissions.BasePermission):
    message = "You do not have permission to create, update, read or delete other users orders."

    def has_object_permission(self, request, view, obj):
        print(obj)
        return request.user == obj.order.user
