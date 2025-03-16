from rest_framework import serializers as s

from apps.offer.serializers import OfferRetrieveSerializer
from apps.sale_order.serializers import PaikarSaleOrderRetrieveSerializer, SaleOrderLineSerializer
from core.constants.common import AUDIT_COLUMNS

from ..models import OrderLine

__all__ = ["OrderLineBaseModelSerializer", "OrderLineCreateUpdateSerializer"]


class OrderLineBaseModelSerializer(s.ModelSerializer):
    class Meta:
        model = OrderLine
        exclude = AUDIT_COLUMNS


class OrderLineCreateUpdateSerializer(OrderLineBaseModelSerializer):
    class Meta:
        model = OrderLine
        exclude = AUDIT_COLUMNS + ("order",)


class OrderLineRetrieveSerializer(OrderLineBaseModelSerializer):
    sale_order = PaikarSaleOrderRetrieveSerializer(read_only=True)
    sale_order_line = SaleOrderLineSerializer(read_only=True)
    offer_sale_order = OfferRetrieveSerializer(read_only=True)

    class Meta:
        model = OrderLine
        exclude = AUDIT_COLUMNS
