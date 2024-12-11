# Register your models here.
from django.contrib import admin

from .models import Address


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = (
        "content_type",
        "object_id",
        "district",
        "division",
        "country",
        "is_active",
    )
    list_per_page = 25
