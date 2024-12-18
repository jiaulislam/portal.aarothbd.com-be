from django.contrib import admin

from core.admin import BaseAdmin

from .models import District


@admin.register(District)
class DistrictAdmin(BaseAdmin):
    list_display = ("name", "bn_name", "division", "is_active")
    list_filter = ("is_active", "division__name")
    search_fields = ("name", "bn_name")
    list_per_page = 25
