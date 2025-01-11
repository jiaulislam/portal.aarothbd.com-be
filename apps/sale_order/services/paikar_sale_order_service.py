from core.services import BaseModelService

from ..models import PaikarSaleOrder


class PaikarSaleOrderService(BaseModelService):
    model_class = PaikarSaleOrder
