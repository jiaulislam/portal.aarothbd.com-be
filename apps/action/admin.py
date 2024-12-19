from django.contrib import admin

from core.admin import BaseAdmin
from core.constants import AUDIT_COLUMNS

from .models import Action


@admin.register(Action)
class ActionAdmin(BaseAdmin):
    list_display = ("codename", "name", "is_active")
    list_filter = ("is_active",)
    search_fields = ("codename", "name")
    readonly_fields = AUDIT_COLUMNS
