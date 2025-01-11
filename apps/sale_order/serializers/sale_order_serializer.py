from rest_framework import serializers as s

from core.constants.common import AUDIT_COLUMNS

from ..models import PaikarSaleOrder


class PaikarSaleOrderBaseModelSerializer(s.ModelSerializer):
    class Meta:
        model = PaikarSaleOrder
        exclude = AUDIT_COLUMNS


class PaikarSaleOrderCreateSerializer(s.ModelSerializer):
    class Meta:
        model = PaikarSaleOrder
        exclude = AUDIT_COLUMNS


class PaikarSaleOrderUpdateSerializer(s.ModelSerializer):
    class Meta:
        model = PaikarSaleOrder
        exclude = AUDIT_COLUMNS
