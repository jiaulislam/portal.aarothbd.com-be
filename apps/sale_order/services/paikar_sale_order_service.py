from core.services import BaseModelService

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

    def create_orderlines(self, orderlines, sale_order_instance, **kwargs):
        orderline_instances = []
        for orderline in orderlines:
            orderline_instance = PaikarSaleOrderLine(**orderline, paikar_sale_order=sale_order_instance)
            orderline_instances.append(orderline_instance)
        self.model_class.objects.bulk_create(orderline_instances)

    def update_orderlines(self, orderlines, sale_order_instance, **kwargs):
        self.model_class.objects.filter(paikar_sale_order=sale_order_instance).delete()
        self.create_orderlines(orderlines, sale_order_instance, **kwargs)
