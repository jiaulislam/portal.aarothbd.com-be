from rest_framework import serializers as s

from ..models import PaikarSaleOrder


class SaleOrderSerializer(s.ModelSerializer):
    class Meta:
        model = PaikarSaleOrder
