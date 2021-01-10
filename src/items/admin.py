from django.contrib import admin

# Register your models here.
from .models import Item


class ItemAdmin(admin.ModelAdmin):
    list_display = ["id", "shop", "name", "slug", "stock"]

    class Meta:
        model = Item


admin.site.register(Item, ItemAdmin)