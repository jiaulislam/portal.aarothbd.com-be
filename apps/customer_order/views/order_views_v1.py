from typing import TYPE_CHECKING

from django.db import transaction
from django.db.models.query import QuerySet
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.generics import ListAPIView, ListCreateAPIView, RetrieveAPIView, UpdateAPIView
from rest_framework.permissions import DjangoModelPermissions, IsAuthenticated
from rest_framework.response import Response
from rest_framework.serializers import BaseSerializer

from core.pagination import ExtendedLimitOffsetPagination
from core.request import Request

from ..serializers import (
    OrderBaseModelSerializer,
    OrderCreateUpdateSerializer,
    OrderListSerializer,
    OrderPaymentCreateUpdateSerializer,
    OrderPaymentListSerializer,
    OrderRetrieveSerializer,
    OrderUpdateStatusSerializer,
)
from ..services import OrderLineService, OrderPaymentService, OrderService

if TYPE_CHECKING:
    from apps.customer_order.models import Order
    from apps.user.models import User


class OrderListCreateAPIView(ListCreateAPIView):
    serializer_class = OrderListSerializer
    permission_classes = [IsAuthenticated]
    order_service = OrderService()
    order_line_service = OrderLineService()
    pagination_class = ExtendedLimitOffsetPagination

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


class OrderUpdateStatusAPIView(UpdateAPIView):
    serializer_class = OrderUpdateStatusSerializer
    permission_classes = [DjangoModelPermissions]
    order_service = OrderService()

    def get_queryset(self):
        return self.order_service.all()

    def update(self, request: Request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = self.get_object()
        order_status = serializer.validated_data.get("order_status")
        date = serializer.validated_data.get("date")
        self.order_service.update_order_status(
            instance,
            order_status,
            date=date,
            request=request,
        )
        response = {"detail": "Order status updated successfully"}
        return Response(response, status=status.HTTP_200_OK)


class OrderPaymentListAPIView(ListAPIView):
    serializer_class = OrderPaymentListSerializer
    permission_classes = [DjangoModelPermissions]
    payment_service = OrderPaymentService()
    pagination_class = ExtendedLimitOffsetPagination

    def get_queryset(self):
        return self.payment_service.all().order_by("-created_at")


class OrderPaymentListCreateAPIView(ListCreateAPIView):
    serializer_class = OrderPaymentCreateUpdateSerializer
    permission_classes = [DjangoModelPermissions]
    payment_service = OrderPaymentService()
    order_service = OrderService()

    def get_queryset(self):
        return self.payment_service.all().order_by("-created_at")

    def list(self, request: Request, order_id: int, *args, **kwargs):
        order = get_object_or_404(Order, id=order_id)
        queryset = order.payments.all().order_by("-created_at")
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request: Request, order_id: int, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        order = get_object_or_404(Order, id=order_id)
        serializer.validated_data["order"] = order
        _ = self.payment_service.create(serializer.validated_data, request=request)
        self.order_service.update_order_amounts(order, serializer.validated_data, request=request)
        response = {"detail": "Payment created successfully"}
        return Response(response, status=status.HTTP_201_CREATED)
