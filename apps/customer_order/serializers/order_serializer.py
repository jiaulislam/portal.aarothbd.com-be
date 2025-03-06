from rest_framework import serializers as s

from core.constants.common import AUDIT_COLUMNS

from ..constants import OrderStatusChoice
from ..models import Order, OrderPayment
from .order_line_serializer import OrderLineCreateUpdateSerializer

__all__ = [
    "OrderBaseModelSerializer",
    "OrderListSerializer",
    "OrderCreateUpdateSerializer",
    "OrderRetrieveSerializer",
    "OrderPaymentListSerializer",
    "OrderPaymentCreateUpdateSerializer",
    "OrderUpdateStatusSerializer",
    "OrderPaymentReversalSerializer",
]


class OrderBaseModelSerializer(s.ModelSerializer):
    class Meta:
        model = Order
        exclude = AUDIT_COLUMNS


class OrderListSerializer(OrderBaseModelSerializer):
    class Meta:
        model = Order
        exclude = AUDIT_COLUMNS


class OrderCreateUpdateSerializer(OrderBaseModelSerializer):
    order_lines = OrderLineCreateUpdateSerializer(many=True, write_only=True)

    class Meta:
        model = Order
        exclude = AUDIT_COLUMNS


class OrderUpdateStatusSerializer(s.Serializer):
    order_status = s.ChoiceField(choices=OrderStatusChoice.choices)
    date = s.DateField(allow_null=True, required=False)


class OrderRetrieveSerializer(OrderBaseModelSerializer):
    order_lines = OrderLineCreateUpdateSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        exclude = AUDIT_COLUMNS


class OrderPaymentListSerializer(s.ModelSerializer):
    order_number = s.CharField(source="order.order_number")

    class Meta:
        model = OrderPayment
        fields = (
            "id",
            "order_number",
            "paymode",
            "payment_date",
            "amount",
        )


class OrderPaymentCreateUpdateSerializer(s.ModelSerializer):
    class Meta:
        model = OrderPayment
        exclude = AUDIT_COLUMNS + (
            "order",
            "is_reversed",
            "reversed_date",
            "reversed_notes",
            "reversed_by",
        )


class OrderPaymentReversalSerializer(s.ModelSerializer):
    class Meta:
        model = OrderPayment
        fields = (
            "id",
            "is_reversed",
            "reversed_date",
            "reversed_notes",
        )
