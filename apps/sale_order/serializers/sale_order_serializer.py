from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers as s

from apps.user.serializers.user_serializer_v1 import UserSerializer
from core.constants.common import AUDIT_COLUMNS

from ..models import PaikarSaleOrder
from .sale_order_line_serializer import SaleOrderLineSerializer


@extend_schema_field(
    {
        "type": "array",
        "items": {"type": "string", "format": "date"},
        "minItems": 2,
        "maxItems": 2,
        "example": ["2023-01-01", "2023-12-31"],
        "description": "A list with exactly two dates: a lower and upper bound.",
    }
)
class DateRangeField(s.ListField):
    """
    Custom field that validates a list with exactly two dates: a lower and upper bound.
    """

    child = s.DateField()

    def to_internal_value(self, data):
        # Validate the input as a list with exactly two items
        data = super().to_internal_value(data)
        if len(data) != 2:
            raise s.ValidationError("This field must contain exactly two dates.")
        if data[0] > data[1]:
            raise s.ValidationError("The lower bound date must be before or equal to the upper bound date.")
        return data

    def to_representation(self, value):
        _range = [value.lower, value.upper]
        return [self.child.to_representation(item) if item is not None else None for item in _range]


class PaikarSaleOrderBaseModelSerializer(s.ModelSerializer):
    validity_dates = DateRangeField()

    class Meta:
        model = PaikarSaleOrder
        exclude = AUDIT_COLUMNS


class PaikarSaleOrderDetailSerializer(s.ModelSerializer):
    validity_dates = DateRangeField()
    orderlines = SaleOrderLineSerializer(many=True, read_only=True)

    class Meta:
        model = PaikarSaleOrder
        exclude = AUDIT_COLUMNS

class PaikarSaleOrderCreateSerializer(s.ModelSerializer):
    order_number = s.CharField(read_only=True)
    order_date = s.DateField(read_only=True)
    company_name = s.CharField(read_only=True)
    status = s.CharField(read_only=True)
    is_active = s.CharField(read_only=True)

    validity_dates = DateRangeField()

    orderlines = SaleOrderLineSerializer(many=True, write_only=True)
    approved_by = UserSerializer(read_only=True)

    class Meta:
        model = PaikarSaleOrder
        exclude = AUDIT_COLUMNS


class PaikarSaleOrderUpdateSerializer(s.ModelSerializer):
    orderlines = SaleOrderLineSerializer(many=True, write_only=True)

    class Meta:
        model = PaikarSaleOrder
        exclude = AUDIT_COLUMNS
