from django.contrib import admin

from core.admin import BaseAdmin
from core.constants import AUDIT_COLUMNS

from .models import BusinessPartner


@admin.register(BusinessPartner)
class BusinessPartnerAdmin(BaseAdmin):
    list_display = (
        "id",
        "name",
        "address",
        "is_active",
    )
    list_filter = ("is_active",)
    readonly_fields = AUDIT_COLUMNS
    list_editable = ("is_active",)
