from typing import TYPE_CHECKING

from django.db import transaction
from django.db.models.query import QuerySet
from rest_framework import status
from rest_framework.generics import ListCreateAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.serializers import BaseSerializer

from core.request import Request

from ..serializers import (
    OrderBaseModelSerializer,
    OrderCreateUpdateSerializer,
    OrderListSerializer,
    OrderRetrieveSerializer,
)
from ..services import OrderLineService, OrderService

if TYPE_CHECKING:
    from apps.customer_order.models import Order
    from apps.user.models import User


class OrderListCreateAPIView(ListCreateAPIView):
    serializer_class = OrderListSerializer
    permission_classes = [IsAuthenticated]
    order_service = OrderService()
    order_line_service = OrderLineService()

    def get_serializer_class(self):
        if self.request.method == "POST":
            return OrderCreateUpdateSerializer
        return OrderListSerializer

    def get_queryset(self):
        current_user: "User" = self.request.user  # type: ignore
        if current_user.is_central_admin:
            return self.order_service.all().order_by("-created_at")
        return self.order_service.all(created_by=current_user).order_by("-created_at")

    @transaction.atomic
    def create(self, request: Request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        order = self.order_service.create_order(serializer.validated_data, request=request)
        serializer = OrderListSerializer(instance=order)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class OrderRetrieveAPIView(RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    lookup_field = "id"
    order_service = OrderService()

    def get_serializer_class(self) -> type[BaseSerializer[OrderBaseModelSerializer]]:
        return OrderRetrieveSerializer

    def get_queryset(self) -> QuerySet["Order"]:
        user: "User" = self.request.user  # type: ignore
        if user.is_central_admin:
            return self.order_service.all()
        return self.order_service.all(created_by=user)

    def retrieve(self, request: Request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
