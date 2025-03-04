from datetime import date
from typing import TYPE_CHECKING, Any, Dict, List, Union

from django.db.models import F
from rest_framework import status

from core.exceptions.common import CustomException
from core.services import BaseModelService

from ..constants import OrderStatusChoice, PaymentStatusChoice
from ..models import Order, OrderPayment

if TYPE_CHECKING:
    from apps.offer.models import Cupon


__all__ = ["OrderService"]


class OrderService(BaseModelService[Order]):
    model_class = Order

    def prepare_data(self, data, *args, **kwargs):
        from apps.sale_order.services import SaleOrderNumberService, SaleOrderPrefixChoices

        sale_order_number_service = SaleOrderNumberService()

        _today = date.today()

        validated_data = data
        validated_data["order_status"] = OrderStatusChoice.PENDING
        validated_data["payment_status"] = PaymentStatusChoice.UNPAID
        validated_data["order_number"] = sale_order_number_service.get_sale_order_sequence(
            SaleOrderPrefixChoices.CUSTOMER,
            _today,
        )
        return validated_data

    def create_order(self, data: Dict[str, Any], **kwargs) -> Order:
        from apps.customer_order.services import OrderLineService

        order_line_service = OrderLineService()

        request = kwargs.get("request")
        order_lines_data = data.pop("order_lines", [])
        validated_data = self.prepare_data(data)
        validated_data["order_total"] = self.calculate_order_total(validated_data, order_lines_data)
        validated_data["discount_amount"] = self.calculate_discount(validated_data)
        validated_data["pay_amount"] = self.calculate_pay_amount(validated_data)
        validated_data["due_amount"] = validated_data["pay_amount"]
        order = self.create(validated_data, request=request)
        order_line_service.bulk_create(order_lines_data, order=order, request=request)
        return order

    def calculate_pay_amount(self, validated_data: Dict[str, Any]) -> float:
        pay_amount = validated_data.get("order_total", 0) - validated_data.get("discount_amount", 0)
        return pay_amount

    def calculate_order_total(self, order_data: Dict[str, Any], validated_order_lines: List[Dict[str, Any]]):
        order_total = 0
        if not bool(validated_order_lines):
            return order_total

        for order_line in validated_order_lines:
            order_total += order_line.get("sub_total", 0)

        order_total += order_data.get("shipping_fee", 0)
        order_total += order_data.get("tax", 0)

        return order_total

    def calculate_discount(self, validated_data: Dict[str, Any]) -> float:
        cupon: Union["Cupon", None] = validated_data.get("cupon_code", None)
        discount_amount = 0

        if not bool(cupon):
            # check if cupon is applied
            return discount_amount

        if not cupon.is_active:
            # check if cupon is active
            exc = CustomException("Cupon is not active", code="client_error")
            exc.status_code = status.HTTP_400_BAD_REQUEST
            raise exc

        discount_amount = cupon.get_discount_amount(validated_data.get("order_total", 0))
        return discount_amount

    def update_order_amounts(self, order: Order, payment_validated_data: Dict[str, Any], **kwargs) -> Order:
        if order.due_amount == 0:
            # check if order is already paid
            exc = CustomException("order is already paid !", code="client_error")
            exc.status_code = status.HTTP_400_BAD_REQUEST
            raise exc
        order.paid_amount = F("paid_amount") + payment_validated_data.get("amount", 0)
        order.due_amount = F("pay_amount") - order.paid_amount
        order.payment_status = PaymentStatusChoice.PAID if order.due_amount == 0 else PaymentStatusChoice.PARTIAL
        order.save()
        return order

    def update_order_status(self, order: Order, status: OrderStatusChoice, **kwargs) -> Order:
        order.order_status = status
        if status == OrderStatusChoice.SHIPPED:
            order.shipped_date = kwargs.get("shipped_date", date.today())
        if status == OrderStatusChoice.DELIVERED:
            order.delivered_date = kwargs.get("delivered_date", date.today())
        order.save()
        return order


class OrderPaymentService(BaseModelService[OrderPayment]):
    model_class = OrderPayment

    def prepare_data(self, data, *args, **kwargs):
        validated_data = data

        return validated_data

    def create_order_payment(self, data: Dict[str, Any], order: Order, **kwargs) -> OrderPayment:
        request = kwargs.get("request")
        validated_data = self.prepare_data(data)
        validated_data["order"] = order
        return self.create(validated_data, request=request)
