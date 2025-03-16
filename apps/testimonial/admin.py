from django.contrib import admin

from core.admin import BaseAdmin
from core.constants import AUDIT_COLUMNS

from .models import Testimonial


@admin.register(Testimonial)
class TestimonialAdmin(BaseAdmin):
    list_display = (
        "id",
        "client_name",
        "client_position",
        "is_active",
    )
    list_filter = ("is_active",)
    readonly_fields = AUDIT_COLUMNS
    list_editable = ("is_active",)
