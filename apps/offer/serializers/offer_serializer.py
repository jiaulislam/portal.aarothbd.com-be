from rest_framework import serializers as s

from ..models import Offer

__all__ = [
    "OfferListSerializer",
    "OfferCreateUpdateSerializer",
    "OfferDetailSerializer",
    "OfferUpdateStatusSerializer",
]


class OfferListSerializer(s.ModelSerializer):
    class Meta:
        model = Offer
        fields = "__all__"


class OfferDetailSerializer(s.ModelSerializer):
    class Meta:
        model = Offer
        fields = "__all__"


class OfferCreateUpdateSerializer(s.ModelSerializer):
    class Meta:
        model = Offer
        fields = "__all__"


class OfferUpdateStatusSerializer(s.ModelSerializer):
    id = s.ReadOnlyField()

    class Meta:
        model = Offer
        fields = ["is_active", "id"]
