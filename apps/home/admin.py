from django.contrib import admin

from core.admin import BaseAdmin
from core.constants import AUDIT_COLUMNS

from .models import Banner


@admin.register(Banner)
class BannerAdmin(BaseAdmin):
    list_display = (
        "id",
        "title",
        "link",
        "order",
        "ad_mode",
        "is_active",
    )
    list_filter = ("is_active",)
    readonly_fields = AUDIT_COLUMNS
    list_editable = ("is_active",)
