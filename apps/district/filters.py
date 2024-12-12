from django_filters import OrderingFilter

from core.filter import BaseFilter

from .models import District


class DistrictFilter(BaseFilter):
    order_by = OrderingFilter(
        fields=(("name", "name"),),
        field_kwargs={
            "name": "Name",
        },
    )

    class Meta:
        model = District
        exclude = ["created_at", "updated_at", "created_by", "updated_by"]
