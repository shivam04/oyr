from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import (
    Order,
    ItemOrder
)


class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'shop', 'order_number', 'pickup_time', 'status']

    class Meta:
        model = Order


class ItemOrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'item', 'order', 'quantity']

    class Meta:
        model = ItemOrder


admin.site.register(Order, OrderAdmin)
admin.site.register(ItemOrder, ItemOrderAdmin)
