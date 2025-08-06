from rest_framework import serializers

from .models import Stock, StockMovement


class StockSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stock
        fields = "__all__"
        read_only_fields = ("id", "created_at", "updated_at")

    def validate(self, attrs):
        if attrs.get("quantity", 0) < 0:
            raise serializers.ValidationError("Quantity cannot be negative.")
        return attrs


class StockMovementSerializer(serializers.ModelSerializer):
    class Meta:
        model = StockMovement
        fields = "__all__"
        read_only_fields = ("id", "created_at", "updated_at")

    def validate(self, attrs):
        if attrs.get("quantity", 0) == 0:
            raise serializers.ValidationError("Quantity cannot be zero.")
        return attrs
