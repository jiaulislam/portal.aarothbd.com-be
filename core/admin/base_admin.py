from django.contrib import admin
from django.forms.models import ModelForm
from django.http import HttpRequest

from ..models import BaseModel

__all__ = ['BaseAdmin']

class BaseAdmin(admin.ModelAdmin):

    def save_model(self, request: HttpRequest, obj: BaseModel, form: ModelForm, change: bool) -> None:
        if change:
            obj.updated_by = request.user  # type: ignore
        else:
            obj.created_by = request.user  # type: ignore
        return super().save_model(request, obj, form, change)
