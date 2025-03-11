from django_filters import rest_framework as filters

from core.filter import BaseFilter

from .models import Offer


class OfferFilter(BaseFilter):
    name = filters.CharFilter(field_name="name", lookup_expr="icontains")
    slug = filters.CharFilter(field_name="slug", lookup_expr="iexact")
    company = filters.CharFilter(field_name="company__slug", lookup_expr="iexact")
    product = filters.CharFilter(field_name="product__slug", lookup_expr="iexact")
    price = filters.RangeFilter(field_name="offer_price")

    class Meta:
        model = Offer
        fields = (
            "name",
            "slug",
            "company",
            "is_active",
            "company_agreed",
            "product",
            "price",
        )
