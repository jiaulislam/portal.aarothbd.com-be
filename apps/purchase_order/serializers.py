from rest_framework import serializers

from apps.company.serializers.company_serializer_v1 import CompanySerializer
from apps.product.serializers.product_serializer import ProductSerializer

from .models import PurchaseOrder, PurchaseOrderLine


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


class PurchaseOrderLineRetrieveCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = PurchaseOrderLine
        fields = ("product", "quantity", "trade_price", "mrp")
        read_only_fields = ("id", "created_at", "updated_at")

    def validate(self, attrs):
        if attrs.get("quantity", 0) <= 0:
            raise serializers.ValidationError("Quantity must be greater than zero.")
        if attrs.get("trade_price", 0.0) < 0:
            raise serializers.ValidationError("Trade price cannot be negative.")
        if attrs.get("mrp", 0.0) < 0:
            raise serializers.ValidationError("MRP cannot be negative.")
        return attrs


class PurchaseOrderSerializer(serializers.ModelSerializer):
    order_lines = PurchaseOrderLineRetrieveCreateSerializer(many=True, required=True)

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


class PurchaseOrderLineRetrieveSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)

    class Meta:
        model = PurchaseOrderLine
        fields = ("product", "quantity", "trade_price", "mrp")
        read_only_fields = ("id", "created_at", "updated_at")


class PurchaseOrderRetrieveSerializer(serializers.ModelSerializer):
    order_lines = PurchaseOrderLineRetrieveSerializer(many=True, read_only=True)

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
