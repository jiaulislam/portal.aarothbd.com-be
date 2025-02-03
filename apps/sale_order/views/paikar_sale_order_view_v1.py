from datetime import datetime
from typing import TYPE_CHECKING

from django.db import transaction
from django.db.models import QuerySet
from rest_framework import status
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateAPIView
from rest_framework.permissions import DjangoModelPermissions
from rest_framework.response import Response
from rest_framework.serializers import BaseSerializer

from core.pagination import ExtendedLimitOffsetPagination
from core.request import Request

from ..constants import SaleOrderPrefixChoices
from ..filters import PaikarSaleOrderFilter
from ..serializers.sale_order_serializer import (
    PaikarSaleOrderApprovalSerializer,
    PaikarSaleOrderBaseModelSerializer,
    PaikarSaleOrderCreateSerializer,
    PaikarSaleOrderDetailSerializer,
    PaikarSaleOrderUpdateSerializer,
)
from ..services import PaikarSaleOrderLineService, PaikarSaleOrderService, SaleOrderNumberService

if TYPE_CHECKING:
    from apps.sale_order.models import PaikarSaleOrder


class PaikarSaleOrderListCreateAPIView(ListCreateAPIView):
    filterset_class = PaikarSaleOrderFilter
    pagination_class = ExtendedLimitOffsetPagination
    permission_classes = [DjangoModelPermissions]

    sale_order_number_service = SaleOrderNumberService()
    sale_order_service = PaikarSaleOrderService()
    sale_order_line_service = PaikarSaleOrderLineService()

    def get_serializer_class(self) -> type[BaseSerializer[PaikarSaleOrderBaseModelSerializer]]:
        if self.request.method == "POST":
            return PaikarSaleOrderCreateSerializer
        return PaikarSaleOrderBaseModelSerializer

    def get_queryset(self) -> QuerySet["PaikarSaleOrder"]:
        queryset = self.sale_order_service.all()
        filterset = self.filterset_class(self.request.GET, queryset=queryset)
        return filterset.qs

    def list(self, request: Request, *args, **kwargs) -> Response:
        queryset = self.get_queryset()
        paginate = self.pagination_class()  # type: ignore
        paginated_queryset = paginate.paginate_queryset(queryset, request)
        serialized = PaikarSaleOrderBaseModelSerializer(paginated_queryset, many=True)
        return paginate.get_paginated_response(serialized.data)

    @transaction.atomic
    def create(self, request: Request, *args, **kwargs) -> Response:
        serialized = self.get_serializer_class()(data=request.data)
        serialized.is_valid(raise_exception=True)

        orderlines = serialized.validated_data.pop("orderlines", [])

        _today = datetime.now().date()
        sale_order_number = self.sale_order_number_service.get_sale_order_sequence(
            SaleOrderPrefixChoices.PAIKAR,
            _today,
        )
        serialized.validated_data["order_number"] = sale_order_number.get_order_number()
        serialized.validated_data["order_date"] = _today

        sale_order_instance = self.sale_order_service.create(serialized.validated_data, request=request)

        # handle orderlines
        self.sale_order_line_service.create_orderlines(orderlines, sale_order_instance, request=request)

        serialized = PaikarSaleOrderBaseModelSerializer(instance=sale_order_instance)
        return Response(serialized.data, status=status.HTTP_201_CREATED)


class PaikarSaleOrderRetrieveUpdateAPIView(RetrieveUpdateAPIView):
    http_method_names = ["get", "put"]
    lookup_field = "id"
    permission_classes = [DjangoModelPermissions]

    sale_order_service = PaikarSaleOrderService()
    sale_order_line_service = PaikarSaleOrderLineService()

    def get_serializer_class(self) -> type[BaseSerializer[PaikarSaleOrderBaseModelSerializer]]:
        if self.request.method == "PUT":
            return PaikarSaleOrderUpdateSerializer
        return PaikarSaleOrderDetailSerializer

    def get_queryset(self) -> QuerySet["PaikarSaleOrder"]:
        return self.sale_order_service.all()

    def retrieve(self, request: Request, *args, **kwargs) -> Response:
        instance = self.get_object()
        serialized = self.get_serializer_class()(instance=instance)
        return Response(serialized.data)

    @transaction.atomic
    def update(self, request: Request, *args, **kwargs) -> Response:
        instance = self.get_object()
        serialized = self.get_serializer_class()(instance, data=request.data)
        serialized.is_valid(raise_exception=True)
        orderlines = serialized.validated_data.pop("orderlines", [])

        sale_order_instance = self.sale_order_service.update(instance, serialized.validated_data, request=request)

        # handle orderlines
        self.sale_order_line_service.update_orderlines(orderlines, sale_order_instance, request=request)

        serialized = self.get_serializer_class()(instance=sale_order_instance)
        return Response(serialized.data)


class PaikarSaleOrderApprovalAPIView(RetrieveUpdateAPIView):
    http_method_names = ["patch"]
    lookup_field = "id"
    permission_classes = [DjangoModelPermissions]
    serializer_class = PaikarSaleOrderApprovalSerializer

    sale_order_service = PaikarSaleOrderService()
    sale_order_line_service = PaikarSaleOrderLineService()

    def get_queryset(self):
        return self.sale_order_service.all()

    def partial_update(self, request: Request, *args, **kwargs) -> Response:
        serializer = self.get_serializer_class()(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = self.get_object()
        instance = self.sale_order_service.approve_sale_order(instance, serializer.validated_data, request=request)
        serialized = self.get_serializer_class()(instance=instance)
        return Response(serialized.data, status=status.HTTP_200_OK)
