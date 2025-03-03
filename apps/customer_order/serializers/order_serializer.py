from rest_framework import serializers as s

from core.constants.common import AUDIT_COLUMNS

from ..models import Order
from .order_line_serializer import OrderLineCreateUpdateSerializer

__all__ = [
    "OrderBaseModelSerializer",
    "OrderListSerializer",
    "OrderCreateUpdateSerializer",
    "OrderRetrieveSerializer",
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


class OrderRetrieveSerializer(OrderBaseModelSerializer):
    order_lines = OrderLineCreateUpdateSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        exclude = AUDIT_COLUMNS
