from core.constants.common import AUDIT_COLUMNS
from core.filter import BaseFilter

from .models import PaikarSaleOrder


class PaikarSaleOrderFilter(BaseFilter):
    class Meta:
        model = PaikarSaleOrder
        exclude = AUDIT_COLUMNS + ("validity_dates",)
