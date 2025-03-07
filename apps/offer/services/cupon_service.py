from typing import Tuple

from core.exceptions.common import CustomException
from core.services import BaseModelService

from ..constants import DiscountPriceMode
from ..models import Cupon

__all__ = ["CuponService"]


class CuponService(BaseModelService[Cupon]):
    model_class = Cupon

    def get_valid_cupons(self, **kwargs):
        queryset = self.model_class.objects.filter(is_active=True, **kwargs)
        return queryset

    def get_discount_amount(self, instance: Cupon, total_amount: float) -> float:
        if instance.discount_mode == DiscountPriceMode.FIXED:
            return instance.discount_amount
        return round((instance.discount_amount / 100) * total_amount)

    def validate_cupon(self, cupon_code: str, total_amount: float) -> Tuple[Cupon, float]:
        """validate the cupon code and return the discount amount"""
        cupon = self.all(cupon_code=cupon_code).first()
        if not cupon:
            raise CustomException("Invalid Cupon Code", code="client_error")
        if not cupon.is_valid():
            raise CustomException("Cupon Expired", code="client_error")

        discount_amount = self.get_discount_amount(cupon, total_amount)
        return cupon, discount_amount
