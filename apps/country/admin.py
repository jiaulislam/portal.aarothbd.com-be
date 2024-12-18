from django.contrib import admin

from core.admin import BaseAdmin

from .models import Country


@admin.register(Country)
class CountryAdmin(BaseAdmin):
    list_display = ("name", "country_code", "continent_name", "is_active")
    list_filter = ("is_active", "continent_name")
    search_fields = ("name", "continent_name", "country_code", "continent_code", "country_code_alpha3")
    list_per_page = 25
