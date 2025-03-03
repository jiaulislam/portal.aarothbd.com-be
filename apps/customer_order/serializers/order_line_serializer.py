from rest_framework import serializers as s

from core.constants.common import AUDIT_COLUMNS

from ..models import OrderLine

__all__ = ["OrderLineBaseModelSerializer", "OrderLineCreateUpdateSerializer"]


class OrderLineBaseModelSerializer(s.ModelSerializer):
    class Meta:
        model = OrderLine
        exclude = AUDIT_COLUMNS


class OrderLineCreateUpdateSerializer(OrderLineBaseModelSerializer):
    class Meta:
        model = OrderLine
        exclude = AUDIT_COLUMNS + ("order",)
