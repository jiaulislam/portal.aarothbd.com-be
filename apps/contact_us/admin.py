from django.contrib import admin

from core.admin import BaseAdmin
from core.constants import AUDIT_COLUMNS

from .models import ContactUs, EmailRecepient


@admin.register(ContactUs)
class ContactUsAdmin(BaseAdmin):
    list_display = (
        "id",
        "name",
        "subject",
        "is_active",
    )
    list_filter = ("is_active",)
    readonly_fields = AUDIT_COLUMNS
    list_editable = ("is_active",)


@admin.register(EmailRecepient)
class EmailRecepientAdmin(BaseAdmin):
    list_display = (
        "id",
        "to_email",
        "is_active",
    )
    readonly_fields = AUDIT_COLUMNS
