from django_filters import OrderingFilter
from django_filters import rest_framework as filters

from core.filter import BaseFilter


class CompanyFilter(BaseFilter):
    name = filters.CharFilter(field_name="name", lookup_expr="icontains")
    slug = filters.CharFilter(field_name="slug", lookup_expr="icontains")
    bin_number = filters.CharFilter(field_name="bin_number", lookup_expr="icontains")
    tin_number = filters.CharFilter(field_name="tin_number", lookup_expr="icontains")
    category = filters.NumberFilter(field_name="category", lookup_expr="exact")

    order_by = OrderingFilter(
        fields=(
            ("name", "name"),
            ("slug", "slug"),
        ),
        field_labels={
            "name": "Name",
            "slug": "Slug",
        },
    )
