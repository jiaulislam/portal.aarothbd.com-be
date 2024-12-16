from django.db import transaction
from django.db.models import QuerySet
from rest_framework import status
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateAPIView, UpdateAPIView
from rest_framework.request import Request
from rest_framework.response import Response

from apps.address.services import AddressService
from apps.product.services import ProductService
from core.pagination import ExtendedLimitOffsetPagination

from ..filters import CompanyFilter
from ..models import Company
from ..serializers.company_serializer_v1 import (
    CompanyCreateSerializer,
    CompanyDetailSerializer,
    CompanyUpdateSerializer,
    CompanyUpdateStatusSerializer,
)
from ..services import CompanyConfigurationService, CompanyService


class CompanyListCreateAPIView(ListCreateAPIView):
    serializer_class = CompanyCreateSerializer
    filterset_class = CompanyFilter
    pagination_class = ExtendedLimitOffsetPagination

    company_service = CompanyService()
    address_service = AddressService()
    company_configuration_service = CompanyConfigurationService()
    product_service = ProductService()

    def get_queryset(self, **kwargs) -> QuerySet[Company]:
        queryset = self.company_service.all(**kwargs).select_related("configuration")
        filterset = self.filterset_class(self.request.GET, queryset=queryset)
        return filterset.qs

    def list(self, request: Request, *args, **kwargs) -> Response:
        queryset = self.get_queryset(**kwargs)
        paginate = self.pagination_class()  # type: ignore
        paginated_queryset = paginate.paginate_queryset(queryset, request)
        serialized = self.serializer_class(paginated_queryset, many=True)  # type: ignore
        return paginate.get_paginated_response(serialized.data)

    @transaction.atomic
    def create(self, request: Request, *args, **kwargs) -> Response:
        serialized = self.serializer_class(data=request.data)  # type: ignore
        serialized.is_valid(raise_exception=True)
        allowed_products = serialized.validated_data.pop("allowed_products", [])
        company_instance = self.company_service.create(serialized.data, request=request)

        # create company configuration
        configuration_data = serialized.validated_data.get("configuration", {})
        configuration_data["company"] = company_instance
        self.company_configuration_service.create(configuration_data, request=request)

        # create addresses
        address_data = serialized.validated_data.get("addresses", [])
        self.address_service.create_company_addresses(address_data, company_instance, request=request)
        serialized = self.serializer_class(instance=company_instance)  # type: ignore

        # assign products
        if allowed_products:
            company_instance.allowed_products.set(allowed_products)
        return Response(serialized.data, status=status.HTTP_201_CREATED)


class CompanyRetrieveUpdateAPIView(RetrieveUpdateAPIView):
    http_method_names = ["get", "put"]
    serializer_class = CompanyUpdateSerializer
    detail_serializer_class = CompanyDetailSerializer

    company_service = CompanyService()
    company_configuration_service = CompanyConfigurationService()

    def retrieve(self, request: Request, *args, **kwargs) -> Response:
        _company_id = kwargs.get("id")
        queryset = self.company_service.get(id=_company_id, select_related=["configuration"])
        serialized = self.detail_serializer_class(queryset)  # type: ignore
        return Response(serialized.data, status=status.HTTP_200_OK)

    @transaction.atomic
    def update(self, request: Request, *args, **kwargs):
        company_serialized = self.serializer_class(data=request.data)  # type: ignore
        company_serialized.is_valid(raise_exception=True)
        allowed_products = company_serialized.validated_data.pop("allowed_products", [])
        # get and update company
        company_instance = self.company_service.get(**kwargs)
        _ = self.company_service.update(
            company_instance,
            company_serialized.validated_data,
            request=request,
        )

        # update products
        if allowed_products:
            company_instance.allowed_products.set(allowed_products)

        response_data = {"detail": "Company Updated successfully."}
        return Response(response_data, status=status.HTTP_200_OK)


class CompanyUpdateStatusAPIView(UpdateAPIView):
    http_method_names = ["patch"]
    serializer_class = CompanyUpdateStatusSerializer

    company_service = CompanyService()

    def partial_update(self, request: Request, *args, **kwargs):
        serialized = self.serializer_class(data=request.data)  # type: ignore
        serialized.is_valid(raise_exception=True)
        instance = self.company_service.get(**kwargs)
        self.company_service.update(instance, serialized.validated_data, request=request)
        return Response({"detail": "Company Status updated."}, status=status.HTTP_200_OK)
