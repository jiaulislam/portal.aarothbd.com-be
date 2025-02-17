from django_filters import rest_framework as filters

from core.filter import BaseFilter

from .models import Offer


class OfferFilter(BaseFilter):
    name = filters.CharFilter(field_name="name", lookup_expr="icontains")
    slug = filters.CharFilter(field_name="slug", lookup_expr="iexact")

    class Meta:
        model = Offer
        fields = (
            "name",
            "slug",
            "company",
            "is_active",
        )
