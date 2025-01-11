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

from ..filters import PaikarSaleOrderFilter
from ..serializers.sale_order_serializer import (
    PaikarSaleOrderBaseModelSerializer,
    PaikarSaleOrderCreateSerializer,
    PaikarSaleOrderUpdateSerializer,
)
from ..services.paikar_sale_order_service import PaikarSaleOrderLineService, PaikarSaleOrderService

if TYPE_CHECKING:
    from apps.sale_order.models import PaikarSaleOrder


class PaikarSaleOrderListCreateAPIView(ListCreateAPIView):
    filterset_class = PaikarSaleOrderFilter
    pagination_class = ExtendedLimitOffsetPagination
    permission_classes = [DjangoModelPermissions]

    sale_order_service = PaikarSaleOrderService()
    sale_order_line_service = PaikarSaleOrderLineService()

    def get_serializer_class(self) -> type[BaseSerializer[PaikarSaleOrderBaseModelSerializer]]:
        if self.request.method == "POST":
            return PaikarSaleOrderCreateSerializer
        return PaikarSaleOrderBaseModelSerializer

    def get_queryset(self) -> QuerySet[PaikarSaleOrder]:
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
        orderlines = request.data.pop("orderlines", [])

        serialized.is_valid(raise_exception=True)
        sale_order_instance = self.sale_order_service.create(serialized.data, request=request)

        # handle orderlines
        self.sale_order_line_service.create_orderlines(orderlines, sale_order_instance, request=request)

        serialized = PaikarSaleOrderBaseModelSerializer(instance=sale_order_instance)
        return Response(serialized.data, status=status.HTTP_201_CREATED)


class PaikarSaleOrderRetrieveUpdateAPIView(RetrieveUpdateAPIView):
    http_method_names = ["GET", "PUT"]
    lookup_field = "id"
    permission_classes = [DjangoModelPermissions]

    sale_order_service = PaikarSaleOrderService()
    sale_order_line_service = PaikarSaleOrderLineService()

    def get_serializer_class(self) -> type[BaseSerializer[PaikarSaleOrderBaseModelSerializer]]:
        if self.request.method == "PUT":
            return PaikarSaleOrderUpdateSerializer
        return PaikarSaleOrderBaseModelSerializer

    def get_queryset(self) -> QuerySet[PaikarSaleOrder]:
        return self.sale_order_service.all()

    def retrieve(self, request: Request, *args, **kwargs) -> Response:
        instance = self.get_object()
        serialized = PaikarSaleOrderBaseModelSerializer(instance=instance)
        return Response(serialized.data)

    @transaction.atomic
    def update(self, request: Request, *args, **kwargs) -> Response:
        instance = self.get_object()
        serialized = self.get_serializer_class()(instance, data=request.data)
        serialized.is_valid(raise_exception=True)
        orderlines = request.data.pop("orderlines", [])

        sale_order_instance = self.sale_order_service.update(instance, serialized.data, request=request)

        # handle orderlines
        self.sale_order_line_service.create_orderlines(orderlines, sale_order_instance, request=request)

        serialized = PaikarSaleOrderBaseModelSerializer(instance=sale_order_instance)
        return Response(serialized.data)
