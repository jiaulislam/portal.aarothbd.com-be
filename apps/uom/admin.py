from django.contrib import admin

from core.admin import BaseAdmin

from .models import UoM, UoMCategory


class UoMInlineAdmin(admin.TabularInline):
    model = UoM
    extra = 0
    exclude = ("created_by", "updated_by")


@admin.register(UoMCategory)
class UoMCategoryAdmin(BaseAdmin):
    list_display = ["name", "is_active"]
    inlines = [UoMInlineAdmin]
