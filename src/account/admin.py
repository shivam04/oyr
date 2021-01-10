from django.contrib import admin

# Register your models here.
from .models import UserDetails


class UsrDetailsAdmin(admin.ModelAdmin):
    list_display = ["id", "user", "aadhar_card", "contact_no", "is_customer"]

    class Meta:
        model = UserDetails


admin.site.register(UserDetails, UsrDetailsAdmin)
