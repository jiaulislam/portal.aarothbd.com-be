from rest_framework import serializers

from apps.company.serializers.company_serializer_v1 import CompanySerializer
from apps.product.serializers.product_serializer import ProductSerializer

from .models import PurchaseOrder, PurchaseOrderLine


class PurchaseOrderLineSerializer(serializers.ModelSerializer):
    class Meta:
        model = PurchaseOrderLine
        fields = "__all__"
        read_only_fields = ("id", "created_at", "updated_at", "purchase_order")

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
    total_trade_price = serializers.SerializerMethodField()
    total_margin_amount = serializers.SerializerMethodField()
    total_quantity = serializers.SerializerMethodField()
    total_mrp = serializers.SerializerMethodField()

    def get_total_trade_price(self, obj) -> float:
        return obj.total_trade_price

    def get_total_margin_amount(self, obj) -> float:
        return obj.total_margin_amount

    def get_total_quantity(self, obj) -> int:
        return obj.total_quantity

    def get_total_mrp(self, obj) -> float:
        return obj.total_mrp

    class Meta:
        model = PurchaseOrder
        fields = "__all__"
        read_only_fields = (
            "id",
            "order_number",
            "created_at",
            "updated_at",
            "total_trade_price",
            "total_margin_amount",
            "total_quantity",
            "total_mrp",
        )

    def to_representation(self, instance):
        representation = super().to_representation(instance)
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
    supplier = CompanySerializer(read_only=True)
    total_trade_price = serializers.SerializerMethodField()
    total_margin_amount = serializers.SerializerMethodField()
    total_quantity = serializers.SerializerMethodField()
    total_mrp = serializers.SerializerMethodField()

    class Meta:
        model = PurchaseOrder
        fields = "__all__"

    def get_total_trade_price(self, obj) -> float:
        return obj.total_trade_price

    def get_total_margin_amount(self, obj) -> float:
        return obj.total_margin_amount

    def get_total_quantity(self, obj) -> int:
        return obj.total_quantity

    def get_total_mrp(self, obj) -> float:
        return obj.total_mrp
