from django.contrib import admin
from unfold.admin import TabularInline

from core.admin import BaseAdmin

from .models import UoM, UoMCategory


class UoMInlineAdmin(TabularInline):
    model = UoM
    extra = 0
    exclude = ("created_by", "updated_by")


@admin.register(UoMCategory)
class UoMCategoryAdmin(BaseAdmin):
    list_display = ["name", "is_active"]
    inlines = [UoMInlineAdmin]
