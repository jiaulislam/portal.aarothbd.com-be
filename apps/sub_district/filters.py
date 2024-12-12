from core.filter import BaseFilter

from .models import SubDistrict
from django_filters import OrderingFilter


class SubDistrictFilter(BaseFilter):
    order_by = OrderingFilter(
        fields=(("name", "name"),),
        field_kwargs={
            "name": "Name",
        },
    )

    class Meta:
        model = SubDistrict
        exclude = ["created_at", "updated_at", "created_by", "updated_by"]
