from rest_framework import serializers

from core.constants import AUDIT_COLUMNS

from ..models import OrderDelivery, OrderDeliveryBill, OrderDeliveryLine

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
    def to_representation(self, instance):
        from .order_line_serializer import OrderLineRetrieveSerializer

        representation = super().to_representation(instance)
        representation["order_line"] = OrderLineRetrieveSerializer(instance.order_line).data
        return representation

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
        from .order_serializer import OrderBaseModelSerializer

        representation = super().to_representation(instance)
        representation["order"] = OrderBaseModelSerializer(instance.order).data if instance.order else None
        representation["return_for_delivery"] = (
            OrderBaseModelSerializer(instance.return_for_delivery).data if instance.return_for_delivery else None
        )
        return representation

    class Meta:
        model = OrderDelivery
        exclude = AUDIT_COLUMNS
