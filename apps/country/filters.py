from django_filters import OrderingFilter, filters

from core.filter import BaseFilter

from .models import Country


class CountryFilter(BaseFilter):
    name = filters.CharFilter(field_name="name", lookup_expr="icontains")
    order_by = OrderingFilter(
        fields=(
            ("name", "name"),
            ("country_code", "country_code"),
            ("continent_code", "continent_code"),
        ),
        field_labels={
            "name": "Name",
            "country_code": "Country Code",
            "continent_code": "Continent Code",
        },
    )

    class Meta:
        model = Country
        exclude = ["created_at", "updated_at", "created_by", "updated_by"]
