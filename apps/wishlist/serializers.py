from rest_framework import serializers as s

from apps.sale_order.models.sale_order_model import PaikarSaleOrder

from .models import Wishlist, WishlistItem


class WishlistItemSerializer(s.ModelSerializer):
    class Meta:
        model = WishlistItem
        fields = ["id", "product", "company", "added_at"]


class WishlistItemAddRemoveSerializer(s.Serializer):
    sale_order = s.PrimaryKeyRelatedField(queryset=PaikarSaleOrder.objects.all())


class WishlistBaseModelSerializer(s.ModelSerializer):
    class Meta:
        model = Wishlist
        fields = ["id", "user", "created_at"]


class WishlistListSerializer(WishlistBaseModelSerializer):
    items = WishlistItemSerializer(many=True, read_only=True)

    class Meta:
        model = Wishlist
        fields = ["id", "user", "items", "created_at"]


class WishlistCreateUpdateSerializer(WishlistBaseModelSerializer):
    items = WishlistItemSerializer(many=True, write_only=True)

    class Meta:
        model = Wishlist
        fields = ["id", "user", "items", "created_at"]
