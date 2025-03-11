from drf_spectacular.utils import extend_schema_field
from psycopg.types.range import Range
from rest_framework import serializers as s

from core.constants.common import AUDIT_COLUMNS

from ..models import PaikarSaleOrderLine

__all__ = [
    "SaleOrderLineSerializer",
    "SaleOrderLineCreateSerializer",
]


@extend_schema_field(
    {
        "type": "array",
        "items": {"type": "number", "format": "integer"},
        "minItems": 2,
        "maxItems": 2,
        "example": [1, 5],
        "description": "A list with exactly two positive integers: a lower and upper bound.",
    }
)
class PositiveIntegerRangeField(s.ListField):
    """
    Custom field that validates a list with exactly two positive integers: a lower and upper bound.
    """

    child = s.IntegerField(min_value=1)

    def to_internal_value(self, data):
        # Validate the input as a list with exactly two items
        data = super().to_internal_value(data)
        if len(data) != 2:
            raise s.ValidationError("This field must contain exactly two positive integers.")
        if data[0] > data[1]:
            raise s.ValidationError("The lower bound must be less than or equal to the upper bound.")
        return data

    def to_representation(self, value: Range):  # type: ignore
        _range = [value.lower, value.upper]
        return [self.child.to_representation(item) if item is not None else None for item in _range]


class SaleOrderLineSerializer(s.ModelSerializer):
    paikar_sale_order = s.ReadOnlyField(source="paikar_sale_order.id")
    is_active = s.CharField(read_only=True)
    quantity_slab = PositiveIntegerRangeField()
    uom = s.SerializerMethodField()

    def get_uom(self, obj: PaikarSaleOrderLine):
        from apps.uom.serializers import UoMSerializer

        data = UoMSerializer(instance=obj.uom).data
        return data

    class Meta:
        model = PaikarSaleOrderLine
        exclude = AUDIT_COLUMNS


class SaleOrderLineCreateSerializer(s.ModelSerializer):
    paikar_sale_order = s.ReadOnlyField(source="paikar_sale_order.id")
    is_active = s.CharField(read_only=True)
    quantity_slab = PositiveIntegerRangeField()

    class Meta:
        model = PaikarSaleOrderLine
        exclude = AUDIT_COLUMNS
