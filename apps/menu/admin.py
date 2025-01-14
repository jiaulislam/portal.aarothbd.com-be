from django.contrib import admin

from core.admin import BaseAdmin

from .models import NavMenu


@admin.register(NavMenu)
class NavigationMenuAdmin(BaseAdmin):
    list_display = ("code_name", "view_name", "parent_menu", "is_active")
    list_filter = ("is_active", )
    search_fields = ("code_name", "view_name",)
    list_editable = ("is_active", )
