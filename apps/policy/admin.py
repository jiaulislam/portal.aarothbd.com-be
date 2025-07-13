from django.contrib import admin

from core.admin import BaseAdmin

from .models import PolicyModel


@admin.register(PolicyModel)
class PolicyAdmin(BaseAdmin):
    list_display = ("title", "subtitle", "description", "created_at", "updated_at")
    search_fields = ("title", "subtitle")
    list_filter = ("created_at", "updated_at")
    ordering = ("-created_at",)
    readonly_fields = ("created_at", "updated_at")
