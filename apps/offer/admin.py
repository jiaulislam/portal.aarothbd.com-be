from django.contrib import admin
from django.forms import ValidationError
from django.forms.models import ModelForm

from core.admin import BaseAdmin

from .models import Cupon, Offer


class OfferForm(ModelForm):
    class Meta:
        model = Offer
        fields = "__all__"

    def clean(self):
        cleaned_data = super().clean()
        start_at = cleaned_data.get("start_at")
        end_at = cleaned_data.get("end_at")

        if start_at and end_at and start_at > end_at:
            raise ValidationError(message={"start_at": ValidationError("Start time is exceeding the End time.")})

        return cleaned_data


@admin.register(Offer)
class OfferAdmin(BaseAdmin):
    list_display = (
        "name",
        "start_at",
        "end_at",
        "discount_mode",
        "discount_amount",
        "is_active",
    )
    list_filter = ("is_active",)
    search_fields = ("name",)
    form = OfferForm


@admin.register(Cupon)
class CuponAdmin(BaseAdmin):
    list_display = (
        "cupon_code",
        "discount_mode",
        "discount_amount",
        "is_active",
    )
