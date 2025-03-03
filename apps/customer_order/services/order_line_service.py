from typing import Any, Dict, List

from core.services import BaseModelService

from ..models import Order, OrderLine

__all__ = ["OrderLineService"]


class OrderLineService(BaseModelService[OrderLine]):
    model_class = OrderLine

    def bulk_create(self, order_lines: List[Dict[str, Any]], order: Order, **kwargs):
        user = self.core_service.get_user(request=kwargs.get("request"))
        return self.model_class.objects.bulk_create(
            [self.model_class(**order_line, order=order, created_by=user) for order_line in order_lines]
        )
