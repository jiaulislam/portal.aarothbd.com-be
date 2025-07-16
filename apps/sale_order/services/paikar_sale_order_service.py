from core.services import BaseModelService

from ..constants import DiscountTypeChoices
from ..models import PaikarSaleOrder, PaikarSaleOrderLine


class PaikarSaleOrderService(BaseModelService[PaikarSaleOrder]):
    model_class = PaikarSaleOrder

    def approve_sale_order(self, sale_order_instance, validated_data, **kwargs):
        current_user = self.core_service.get_user(kwargs.get("request"))
        validated_data["approved_by"] = current_user
        instance = self.update(sale_order_instance, validated_data, **kwargs)
        return instance


class PaikarSaleOrderLineService(BaseModelService[PaikarSaleOrderLine]):
    model_class = PaikarSaleOrderLine

    def _get_customer_rate(self, orderline):
        rate = orderline.get("rate", 0)
        margin = orderline.get("margin_amount", 0)
        discount_type = orderline.get("discount_type", DiscountTypeChoices.PERCENTAGE)
        discount_amount = orderline.get("discount_amount", 0)

        if discount_type == DiscountTypeChoices.FIXED:
            return (rate + margin) - discount_amount
        else:
            return rate + margin - (rate * discount_amount / 100)

    def create_orderlines(self, orderlines, sale_order_instance, **kwargs):
        orderline_instances = []
        for orderline in orderlines:
            customer_rate = self._get_customer_rate(orderline)
            orderline["customer_rate"] = customer_rate
            orderline_instance = PaikarSaleOrderLine(**orderline, paikar_sale_order=sale_order_instance)
            orderline_instances.append(orderline_instance)
        self.model_class.objects.bulk_create(orderline_instances)

    def update_orderlines(self, orderlines, sale_order_instance, **kwargs):
        self.model_class.objects.filter(paikar_sale_order=sale_order_instance).delete()
        self.create_orderlines(orderlines, sale_order_instance, **kwargs)
