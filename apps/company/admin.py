from django.contrib import admin
from unfold.admin import TabularInline
from unfold.contrib.inlines.admin import NonrelatedStackedInline

from apps.address.models import Address
from core.admin import BaseAdmin, InlineHelperAdmin
from core.constants import AUDIT_COLUMNS

from .models import Company, CompanyCategory, CompanyConfiguration


class CompanySettingsInline(TabularInline, InlineHelperAdmin):
    model = CompanyConfiguration
    exclude = AUDIT_COLUMNS
    can_delete = False
    show_change_link = True
    verbose_name_plural = "Company Settings"
    verbose_name = "Company Settings"


class AddressInline(NonrelatedStackedInline, InlineHelperAdmin):
    extra = 0
    model = Address
    fk_name = "addresses"
    ct_field = "content_type"
    ct_fk_field = "object_id"
    exclude = AUDIT_COLUMNS
    fields = ("line_1", "line_2", "sub_district", "district", "division", "country", "address_type", "is_default")

    def get_form_queryset(self, obj):
        queryset = self.model.objects.filter(content_type__model="company", object_id=obj.pk)
        return queryset

    def save_new_instance(self, parent, instance):
        """
        Extra save method which can for example update inline instances based on current
        main model object. Method must be implemented.
        """
        pass


@admin.register(CompanyCategory)
class CompanyCategoryAdmin(BaseAdmin):
    list_display = ("name", "is_active")
    search_fields = ("name",)
    list_filter = ("is_active",)
    readonly_fields = AUDIT_COLUMNS
    list_editable = ("is_active",)


@admin.register(Company)
class CompanyAdmin(BaseAdmin):
    list_display = ("name", "slug", "theme_color", "is_active")
    search_fields = ("name", "slug", "tin_number", "bin_number")
    list_filter = ("is_active",)
    inlines = [CompanySettingsInline, AddressInline]
    readonly_fields = AUDIT_COLUMNS
    filter_horizontal = ("allowed_products",)
    list_editable = ("is_active",)
