from typing import Any, Dict

from rest_framework import serializers as s

from core.constants import AUDIT_COLUMNS

from ..constants import DiscountPriceMode
from ..models import Cupon

__all__ = [
    "CuponSerializer",
    "CuponValidateSerializer",
]


class CuponSerializer(s.ModelSerializer):
    class Meta:
        model = Cupon
        exclude = AUDIT_COLUMNS


class CuponValidateSerializer(s.Serializer):
    total_amount = s.FloatField(default=0)
    discount_mode = s.ChoiceField(
        choices=DiscountPriceMode.choices,
        default=DiscountPriceMode.FIXED,
    )

    def validate_discount_mode(self, value: str) -> str:
        if value == DiscountPriceMode.FIXED:
            return value

        if self.data["discount_amount"] > 100:
            raise s.ValidationError("Discount amount should be less than 100 for percentage mode")
        return value

    def validate(self, attrs: Dict[str, Any]) -> Dict[str, Any]:
        discount_mode = attrs.get("discount_mode")
        total_amount = attrs.get("total_amount")

        if discount_mode == DiscountPriceMode.PERCENTAGE and total_amount == 0:
            raise s.ValidationError("Total amount is required when discount mode is percentage")

        return attrs
