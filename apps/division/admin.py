from django.contrib import admin

from .models import Division


@admin.register(Division)
class DivisionAdmin(admin.ModelAdmin):
    list_display = ("name", "bn_name", "is_active")
    list_filter = ("is_active",)
    search_fields = ("name", "bn_name")
    list_per_page = 25
