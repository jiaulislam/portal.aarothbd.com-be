from django_filters import OrderingFilter

from core.filter import BaseFilter

from .models import SubDistrict


class SubDistrictFilter(BaseFilter):
    order_by = OrderingFilter(
        fields=(("name", "name"),),
        field_labels={
            "name": "Name",
        },
    )

    class Meta:
        model = SubDistrict
        exclude = ["created_at", "updated_at", "created_by", "updated_by"]
