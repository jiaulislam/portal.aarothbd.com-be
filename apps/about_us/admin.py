from django.contrib import admin

from core.admin import BaseAdmin
from core.constants import AUDIT_COLUMNS

from .models import AboutUs


@admin.register(AboutUs)
class AboutUsAdmin(BaseAdmin):
    list_display = (
        "id",
        "title",
        "is_active",
    )
    list_filter = ("is_active",)
    readonly_fields = AUDIT_COLUMNS
    list_editable = ("is_active",)
