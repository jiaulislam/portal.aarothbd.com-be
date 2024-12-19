# Register your models here.
from django.contrib import admin

from core.admin import BaseAdmin
from core.constants import AUDIT_COLUMNS

from .models import Address


@admin.register(Address)
class AddressAdmin(BaseAdmin):
    list_display = (
        "content_type",
        "object_id",
        "district",
        "division",
        "country",
        "is_active",
    )
    readonly_fields = AUDIT_COLUMNS
