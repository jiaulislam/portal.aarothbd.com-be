from django.contrib.admin.options import InlineModelAdmin
from django.db import models
from django.forms.models import ModelForm
from django.http import HttpRequest
from unfold.admin import ModelAdmin
from unfold.contrib.forms.widgets import WysiwygWidget

from ..models import BaseModel

__all__ = ["BaseAdmin", "InlineHelperAdmin"]


class InlineHelperAdmin(InlineModelAdmin):
    def get_fields(self, request, obj=None):
        fields = super().get_fields(request, obj)
        if "is_active" in fields:
            fields.remove("is_active")  # type: ignore
            fields.append("is_active")  # type: ignore
        return fields


class BaseAdmin(ModelAdmin):
    formfield_overrides = {
        models.TextField: {
            "widget": WysiwygWidget,
        }
    }

    def get_fields(self, request, obj=None):
        fields = super().get_fields(request, obj)
        if "is_active" in fields:
            fields.remove("is_active")  # type: ignore
            fields.append("is_active")  # type: ignore
        return fields

    def save_model(self, request: HttpRequest, obj: BaseModel, form: ModelForm, change: bool) -> None:
        if change:
            obj.updated_by = request.user  # type: ignore
        else:
            obj.created_by = request.user  # type: ignore
        return super().save_model(request, obj, form, change)  # type: ignore
