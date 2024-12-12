from core.filter import BaseFilter

from .models import Division
from django_filters import OrderingFilter


class DivisionFilter(BaseFilter):
    order_by = OrderingFilter(
        fields=(("name", "name"),),
        field_labels={
            "name": "Name",
        },
    )

    class Meta:
        model = Division
        exclude = ["created_at", "updated_at", "created_by", "updated_by"]
