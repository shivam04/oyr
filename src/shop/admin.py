from django.contrib import admin

# Register your models here.
from .models import Shop


class ShopAdmin(admin.ModelAdmin):
    list_display = ["id", "user", "name", "slug"]

    class Meta:
        model = Shop


admin.site.register(Shop, ShopAdmin)