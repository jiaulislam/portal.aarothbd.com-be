from django_filters import OrderingFilter, filters

from core.filter import BaseFilter

from .models import District


class DistrictFilter(BaseFilter):
    name = filters.CharFilter(field_name="name", lookup_expr="icontains")

    order_by = OrderingFilter(
        fields=(("name", "name"),),
        field_labels={
            "name": "Name",
        },
    )

    class Meta:
        model = District
        exclude = ["created_at", "updated_at", "created_by", "updated_by"]
