from rest_framework import serializers

from core.constants import AUDIT_COLUMNS

from ..models import OrderDelivery, OrderDeliveryBill, OrderDeliveryLine

__all__ = ["OrderDeliverySerializer", "OrderDeliveryLineSerializer", "OrderDeliveryBillSerializer"]


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
