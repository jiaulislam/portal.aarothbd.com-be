from django.contrib import admin
from django.contrib.auth.admin import GroupAdmin as BaseGroupAdmin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group
from django.forms import ModelForm
from django.http import HttpRequest
from django.utils.translation import gettext_lazy as _
from unfold.admin import ModelAdmin, StackedInline

from core.admin import InlineHelperAdmin
from core.constants import AUDIT_COLUMNS

from .constants import UserTypeChoices
from .models import User, UserProfile

admin.site.unregister(Group)


@admin.register(Group)
class GroupAdmin(BaseGroupAdmin, ModelAdmin):
    pass


class UserTypeListFilter(admin.SimpleListFilter):
    title = _("User Type")
    parameter_name = "user_type"

    def lookups(self, request, model_admin):
        _lookups = [(key, _(value)) for key, value in UserTypeChoices.choices]
        return _lookups

    def queryset(self, request, queryset):
        return queryset.filter(user_type=self.value()) if self.value() else queryset


class ProfileInline(StackedInline, InlineHelperAdmin):  # type: ignore
    model = UserProfile
    can_delete = False
    show_change_link = True


@admin.register(UserProfile)
class ProfileAdmin(ModelAdmin):
    list_display = ["user", "bin_id"]


@admin.register(User)
class UserAdmin(BaseUserAdmin, ModelAdmin):
    list_display = (
        "email",
        "date_joined",
        "user_type",
        "company",
        "is_admin",
        "is_superuser",
        "is_active",
    )
    search_fields = ("email", "first_name", "last_name", "user_type")
    inlines = [ProfileInline]
    fieldsets = (
        (None, {"fields": ("user_name", "email", "phone", "password")}),
        (
            _("Personal info"),
            {
                "fields": (
                    "first_name",
                    "last_name",
                    "user_type",
                    "company",
                    "auth_provider",
                )
            },
        ),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_admin",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (
            "New User",
            {
                "classes": ("wide",),
                "fields": ("email", "password1", "password2", "user_type", "company"),
            },
        ),
    )
    ordering = ("date_joined",)
    list_filter = ("is_admin", "is_superuser", "company", UserTypeListFilter)
    filter_horizontal = (
        "groups",
        "user_permissions",
    )
    readonly_fields = AUDIT_COLUMNS
    list_per_page = 10

    def save_model(self, request: HttpRequest, obj: User, form: ModelForm, change: bool) -> None:  # type: ignore
        if change:
            obj.updated_by = request.user  # type: ignore
        else:
            obj.created_by = request.user  # type: ignore
        return super().save_model(request, obj, form, change)  # type: ignore
