from rest_framework import serializers

from apps.company.serializers.company_serializer_v1 import CompanySerializer

from .models import PurchaseOrder, PurchaseOrderLine


class PurchaseOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = PurchaseOrder
        fields = "__all__"
        read_only_fields = ("id", "order_number", "created_at", "updated_at")

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation["total_trade_price"] = instance.total_trade_price
        representation["total_margin_amount"] = instance.total_margin_amount
        representation["total_quantity"] = instance.total_quantity
        representation["total_mrp"] = instance.total_mrp
        representation["supplier"] = CompanySerializer(instance.supplier).data
        return representation


class PurchaseOrderLineSerializer(serializers.ModelSerializer):
    class Meta:
        model = PurchaseOrderLine
        fields = "__all__"
        read_only_fields = ("id", "created_at", "updated_at")

    def validate(self, attrs):
        if attrs.get("quantity", 0) <= 0:
            raise serializers.ValidationError("Quantity must be greater than zero.")
        if attrs.get("trade_price", 0.0) < 0:
            raise serializers.ValidationError("Trade price cannot be negative.")
        if attrs.get("mrp", 0.0) < 0:
            raise serializers.ValidationError("MRP cannot be negative.")
        return attrs
