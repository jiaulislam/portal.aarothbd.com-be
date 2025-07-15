from rest_framework import serializers

from core.constants import AUDIT_COLUMNS

from ..models import OrderDelivery, OrderDeliveryBill, OrderDeliveryLine
from .order_serializer import OrderRetrieveSerializer

__all__ = [
    "OrderDeliverySerializer",
    "OrderDeliveryLineSerializer",
    "OrderDeliveryBillSerializer",
    "OrderDeliveryRetrieveSerializer",
]


class OrderDeliverySerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderDelivery
        exclude = AUDIT_COLUMNS


class OrderDeliveryLineSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderDeliveryLine
        exclude = AUDIT_COLUMNS


class OrderDeliveryBillSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderDeliveryBill
        exclude = AUDIT_COLUMNS


class OrderDeliveryRetrieveSerializer(serializers.ModelSerializer):
    delivery_lines = OrderDeliveryLineSerializer(many=True, read_only=True)
    bill = OrderDeliveryBillSerializer(read_only=True)

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation["order"] = OrderRetrieveSerializer(instance.order).data
        representation["return_for_delivery"] = OrderRetrieveSerializer(instance.return_for_delivery).data
        return representation

    class Meta:
        model = OrderDelivery
        exclude = AUDIT_COLUMNS
