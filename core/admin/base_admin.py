# from django.contrib import admin
from django.db import models
from django.forms.models import ModelForm
from django.http import HttpRequest
from unfold.admin import ModelAdmin
from unfold.contrib.forms.widgets import WysiwygWidget

from ..models import BaseModel

__all__ = ["BaseAdmin"]


class BaseAdmin(ModelAdmin):
    formfield_overrides = {
        models.TextField: {
            "widget": WysiwygWidget,
        }
    }

    def save_model(self, request: HttpRequest, obj: BaseModel, form: ModelForm, change: bool) -> None:
        if change:
            obj.updated_by = request.user  # type: ignore
        else:
            obj.created_by = request.user  # type: ignore
        return super().save_model(request, obj, form, change)  # type: ignore
