from django.db import transaction
from django.db.models import QuerySet
from rest_framework import status
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateAPIView, UpdateAPIView
from rest_framework.permissions import (
    SAFE_METHODS,
    AllowAny,
    DjangoModelPermissions,
    DjangoModelPermissionsOrAnonReadOnly,
    IsAuthenticated,
)
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.serializers import ModelSerializer
from rest_framework.viewsets import ModelViewSet

from apps.address.services import AddressService
from apps.product.services import ProductService
from core.authentication import SecureCookieAuthentication
from core.pagination import ExtendedLimitOffsetPagination

from ..filters import CompanyFilter
from ..models import Company, CompanyCategory
from ..serializers.company_serializer_v1 import (
    CompanyCategorySerializer,
    CompanyCreateSerializer,
    CompanyDetailSerializer,
    CompanyListSerializer,
    CompanyUpdateSerializer,
    CompanyUpdateStatusSerializer,
)
from ..services import CompanyConfigurationService, CompanyService


class CompanyListCreateAPIView(ListCreateAPIView):
    serializer_class = CompanyCreateSerializer
    filterset_class = CompanyFilter
    pagination_class = ExtendedLimitOffsetPagination
    permission_classes = [DjangoModelPermissions, IsAuthenticated]
    authentication_classes = [SecureCookieAuthentication]

    company_service = CompanyService()
    address_service = AddressService()
    company_configuration_service = CompanyConfigurationService()
    product_service = ProductService()

    def get_permissions(self):
        if self.request.method in SAFE_METHODS:
            return [AllowAny()]  # Public access for GET, HEAD, OPTIONS
        return [permission() for permission in self.permission_classes]

    def get_serializer_class(self) -> type[ModelSerializer[Company]]:
        if self.request.method == "POST":
            return CompanyCreateSerializer
        return CompanyListSerializer

    def get_queryset(self, **kwargs) -> QuerySet[Company]:
        queryset = self.company_service.all(**kwargs).select_related("configuration")
        filterset = self.filterset_class(self.request.GET, queryset=queryset)
        return filterset.qs

    def list(self, request: Request, *args, **kwargs) -> Response:
        queryset = self.get_queryset(**kwargs)
        paginate = self.pagination_class()  # type: ignore
        paginated_queryset = paginate.paginate_queryset(queryset, request)
        serialized = self.get_serializer_class()(paginated_queryset, many=True)
        return paginate.get_paginated_response(serialized.data)

    @transaction.atomic
    def create(self, request: Request, *args, **kwargs) -> Response:
        serialized = self.get_serializer_class()(data=request.data)
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

        company_instance.allowed_products.set(allowed_products)
        return Response(serialized.data, status=status.HTTP_201_CREATED)


class CompanyRetrieveUpdateAPIView(RetrieveUpdateAPIView):
    http_method_names = ["get", "put"]
    serializer_class = CompanyDetailSerializer
    permission_classes = [DjangoModelPermissions]

    company_service = CompanyService()
    company_configuration_service = CompanyConfigurationService()

    def get_queryset(self) -> QuerySet["Company"]:
        return self.company_service.all().select_related("configuration")

    def get_serializer_class(self) -> type[ModelSerializer[Company]]:
        if self.request.method == "POST":
            return CompanyUpdateSerializer
        return CompanyDetailSerializer

    def retrieve(self, request: Request, *args, **kwargs) -> Response:
        _company_id = kwargs.get("id")
        queryset = self.company_service.get(id=_company_id, select_related=["configuration"])
        serialized = self.get_serializer_class()(instance=queryset)
        return Response(serialized.data, status=status.HTTP_200_OK)

    @transaction.atomic
    def update(self, request: Request, *args, **kwargs):
        company_serialized = self.get_serializer_class()(data=request.data)
        company_serialized.is_valid(raise_exception=True)
        allowed_products = company_serialized.validated_data.pop("allowed_products", [])
        # get and update company
        company_instance = self.company_service.get(**kwargs)
        _ = self.company_service.update(
            company_instance,
            company_serialized.validated_data,
            request=request,
        )

        company_instance.allowed_products.set(allowed_products)

        response_data = {"detail": "Company Updated successfully."}
        return Response(response_data, status=status.HTTP_200_OK)


class CompanyUpdateStatusAPIView(UpdateAPIView):
    http_method_names = ["patch"]
    serializer_class = CompanyUpdateStatusSerializer
    permission_classes = [DjangoModelPermissions]

    company_service = CompanyService()

    def get_queryset(self) -> QuerySet["Company"]:
        return self.company_service.all()

    def partial_update(self, request: Request, *args, **kwargs):
        serialized = self.serializer_class(data=request.data)  # type: ignore
        serialized.is_valid(raise_exception=True)
        instance = self.company_service.get(**kwargs)
        self.company_service.update(instance, serialized.validated_data, request=request)
        return Response({"detail": "Company Status updated."}, status=status.HTTP_200_OK)


class CompanyCategoryViewSet(ModelViewSet):
    serializer_class = CompanyCategorySerializer
    permission_classes = [DjangoModelPermissionsOrAnonReadOnly]
    pagination_class = ExtendedLimitOffsetPagination

    def get_queryset(self):
        queryset = CompanyCategory.objects.all()
        return queryset
