from typing import Any, Dict

from core.services import BaseModelService

from ..models import Order

__all__ = ["OrderService"]


class OrderService(BaseModelService[Order]):
    model_class = Order

    def create_order(self, validated_data: Dict[str, Any], **kwargs) -> Order:
        from apps.customer_order.services import OrderLineService

        order_line_service = OrderLineService()

        request = kwargs.get("request")
        order_lines_data = validated_data.pop("order_lines", [])
        order = self.create(validated_data, request=request)
        order_line_service.bulk_create(order_lines_data, order=order, request=request)
        return order
