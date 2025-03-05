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
    class Meta:
        model = OrderPayment
        fields = (
            "id",
            "order__order_number",
            "paymode",
            "payment_date",
            "amount",
        )


class OrderPaymentCreateUpdateSerializer(s.ModelSerializer):
    class Meta:
        model = OrderPayment
        exclude = AUDIT_COLUMNS + ("order",)
