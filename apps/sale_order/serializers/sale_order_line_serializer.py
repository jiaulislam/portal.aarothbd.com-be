from rest_framework import serializers as s

from ..models import PaikarSaleOrderLine


class SaleOrderLineSerializer(s.ModelSerializer):
    class Meta:
        model = PaikarSaleOrderLine
