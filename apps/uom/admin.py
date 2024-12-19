from django.contrib import admin
from unfold.admin import TabularInline

from core.admin import BaseAdmin, InlineHelperAdmin
from core.constants import AUDIT_COLUMNS

from .models import UoM, UoMCategory


class UoMInlineAdmin(TabularInline, InlineHelperAdmin):
    model = UoM
    extra = 0
    exclude = AUDIT_COLUMNS


@admin.register(UoMCategory)
class UoMCategoryAdmin(BaseAdmin):
    list_display = ["name", "is_active"]
    inlines = [UoMInlineAdmin]
    readonly_fields = AUDIT_COLUMNS
