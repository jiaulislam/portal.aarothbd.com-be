from drf_spectacular.utils import extend_schema_field
from psycopg.types.range import Range
from rest_framework import serializers as s

from core.constants.common import AUDIT_COLUMNS

from ..models import PaikarSaleOrder, Review
from .sale_order_line_serializer import SaleOrderLineCreateSerializer, SaleOrderLineSerializer

__all__ = [
    "PaikarSaleOrderBaseModelSerializer",
    "PaikarSaleOrderDetailSerializer",
    "PaikarSaleOrderCreateSerializer",
    "PaikarSaleOrderUpdateSerializer",
    "PaikarSaleOrderApprovalSerializer",
    "ReviewSerializer",
    "SaleOrderReviewSerializer",
    "PaikarSaleOrderRetrieveSerializer",
]


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
        if isinstance(value, Range):
            value = [value.lower, value.upper]
        return [self.child.to_representation(item) if item is not None else None for item in value]


class PaikarSaleOrderBaseModelSerializer(s.ModelSerializer):
    validity_dates = DateRangeField()

    class Meta:
        model = PaikarSaleOrder
        exclude = AUDIT_COLUMNS


class PaikarSaleOrderRetrieveSerializer(s.ModelSerializer):
    validity_dates = DateRangeField()
    product = s.SerializerMethodField()

    def get_product(self, obj: PaikarSaleOrder):
        from apps.product.serializers.product_serializer import ProductSerializer

        product = ProductSerializer(obj.product)
        return product.data

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

    orderlines = SaleOrderLineCreateSerializer(many=True, write_only=True)

    def get_approved_by(self, obj):
        from apps.user.serializers.user_serializer_v1 import UserSerializer

        approved_by = UserSerializer(obj.approved_by)
        return approved_by.data

    class Meta:
        model = PaikarSaleOrder
        exclude = AUDIT_COLUMNS


class PaikarSaleOrderUpdateSerializer(s.ModelSerializer):
    orderlines = SaleOrderLineCreateSerializer(many=True, write_only=True)

    class Meta:
        model = PaikarSaleOrder
        exclude = AUDIT_COLUMNS


class PaikarSaleOrderApprovalSerializer(s.ModelSerializer):
    class Meta:
        model = PaikarSaleOrder
        fields = ("status", "remarks", "id")


class ReviewSerializer(s.ModelSerializer):
    class Meta:
        model = Review
        exclude = AUDIT_COLUMNS


class SaleOrderReviewSerializer(s.Serializer):
    reviewer_name = s.CharField()
    reviewer_email = s.EmailField(allow_null=True)
    reviewer_phone = s.CharField(allow_null=True)
    rating = s.IntegerField(min_value=1, max_value=5)
    reviewer_comment = s.CharField(allow_null=True)
    created_at = s.DateTimeField()
