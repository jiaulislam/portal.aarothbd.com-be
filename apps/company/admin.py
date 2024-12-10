from django.contrib import admin

from core.admin import BaseAdmin

from .models import Company, CompanyConfiguration


class CompanySettingsInline(admin.TabularInline):
    model = CompanyConfiguration
    exclude = ("created_by", "updated_by")
    can_delete = False
    show_change_link = True
    verbose_name_plural = "Company Settings"
    verbose_name = "Company Settings"


@admin.register(Company)
class CompanyAdmin(BaseAdmin):
    list_display = ("name", "slug", "theme_color", "is_active")
    search_fields = ("name", "slug", "tin_number", "bin_number")
    list_filter = ("is_active",)
    inlines = (CompanySettingsInline,)
    list_per_page = 10
    readonly_fields = ("created_at", "updated_at", "created_by", "updated_by")
