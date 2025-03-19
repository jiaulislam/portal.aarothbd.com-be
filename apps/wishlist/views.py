from typing import TYPE_CHECKING

from rest_framework import status
from rest_framework.generics import CreateAPIView, ListCreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.product.serializers.product_serializer import ProductEcomSerializer
from core.request import Request

from .models import Wishlist
from .serializers import WishlistItemAddRemoveSerializer

if TYPE_CHECKING:
    from user.models import User


class WishlistItemListCreateAPIView(ListCreateAPIView):
    serializer_class = WishlistItemAddRemoveSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        current_user: "User" = self.request.user  # type: ignore
        if current_user.is_central_admin:
            return Wishlist.objects.all()
        return Wishlist.objects.filter(user=current_user)

    def list(self, request: Request, *args, **kwargs):
        current_user: "User" = request.user  # type: ignore
        wishlist, _ = Wishlist.objects.get_or_create(user=current_user)
        sale_orders = wishlist.get_wishlist_active_sale_orders(current_user)
        serializer = ProductEcomSerializer(instance=sale_orders, many=True)
        return Response(serializer.data)

    def create(self, request: Request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        current_user: "User" = request.user  # type: ignore
        wishlist, _ = Wishlist.objects.get_or_create(user=current_user)

        sale_order = serializer.validated_data.get("sale_order")
        product = sale_order.product
        company = sale_order.company
        wishlist.add_product(product, company)
        response = {"detail": "item added to wishlist successfully."}
        return Response(response, status=status.HTTP_201_CREATED)


class WishlistItemRemoveAPIView(CreateAPIView):
    serializer_class = WishlistItemAddRemoveSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        current_user: "User" = self.request.user  # type: ignore
        if current_user.is_central_admin:
            return Wishlist.objects.all()
        return Wishlist.objects.filter(user=current_user)

    def create(self, request: Request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)  # type: ignore
        serializer.is_valid(raise_exception=True)
        current_user: "User" = request.user  # type: ignore
        wishlist, _ = Wishlist.objects.get_or_create(user=current_user)

        sale_order = serializer.validated_data.get("sale_order")
        wishlist.remove_product(sale_order.product, sale_order.company)
        response = {"detail": "item removed from wishlist successfully."}
        return Response(response, status=status.HTTP_200_OK)
