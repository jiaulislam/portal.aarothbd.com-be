from django.contrib import admin

from core.admin import BaseAdmin

from .models import SubDistrict


@admin.register(SubDistrict)
class SubDistrictAdmin(BaseAdmin):
    list_display = ("name", "bn_name", "district", "is_active")
    list_filter = ("is_active", "district__name")
    search_fields = ("name", "bn_name")
    list_per_page = 25
