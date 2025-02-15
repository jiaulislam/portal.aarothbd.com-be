from typing import TYPE_CHECKING, Any, MutableMapping, Type

from django.db import transaction
from django.db.models.query import QuerySet
from rest_framework import status
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateAPIView, UpdateAPIView
from rest_framework.permissions import DjangoModelPermissions
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.serializers import ModelSerializer

from core.pagination import ExtendedLimitOffsetPagination

from ..filters import ProductFilter
from ..serializers.product_serializer import (
    ProductCreateSerializer,
    ProductExtendedSerializer,
    ProductUpdateSerializer,
    ProductUpdateStatusSerializer,
)
from ..services import ProductBrandService, ProductService

if TYPE_CHECKING:
    from apps.product.models.product_model import Product


class ProductListCreateAPIView(ListCreateAPIView):
    serializer_class = ProductCreateSerializer
    permission_classes = [DjangoModelPermissions]
    product_service = ProductService()
    brand_service = ProductBrandService()
    pagination_class = ExtendedLimitOffsetPagination
    filterset_class = ProductFilter

    def get_queryset(self) -> QuerySet["Product"]:
        return self.product_service.all(select_related=["brand", "category", "origin", "uom"])

    @transaction.atomic
    def create(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        serializer = self.serializer_class(data=request.data)  # type: ignore
        serializer.is_valid(raise_exception=True)

        brand: MutableMapping[str, Any] = serializer.validated_data.pop("brand", {})
        details = serializer.validated_data.pop("details", [])
        # handle brand
        _brand, _ = self.brand_service.get_or_create(brand, request=request)
        serializer.validated_data["brand"] = _brand

        instance = self.product_service.create(serializer.validated_data, request=request)

        # handle detail
        self.product_service.create_product_details(instance, details, request=request)

        serializer = self.serializer_class(instance=instance)  # type: ignore

        return Response(serializer.data, status=status.HTTP_200_OK)


class ProductRetrieveUpdateAPIView(RetrieveUpdateAPIView):
    http_method_names = ["put", "get"]
    permission_classes = [DjangoModelPermissions]
    product_service = ProductService()
    brand_service = ProductBrandService()
    lookup_field = "slug"

    def get_queryset(self) -> QuerySet["Product"]:
        return self.product_service.all()

    def get_serializer_class(self) -> Type[ModelSerializer["Product"]]:
        if self.request.method == "PUT":
            return ProductUpdateSerializer
        return ProductExtendedSerializer

    @transaction.atomic
    def update(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        serializer = ProductUpdateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        brand: MutableMapping[str, Any] = serializer.validated_data.pop("brand", {})
        details = serializer.validated_data.pop("details", [])
        # handle brand
        _brand, _ = self.brand_service.get_or_create(brand, request=request)
        serializer.validated_data["brand"] = _brand

        instance = self.product_service.get(**kwargs)
        instance = self.product_service.update(instance, serializer.validated_data, request=request)

        # handle detail
        self.product_service.update_product_details(instance, details, request=request)

        serializer = ProductExtendedSerializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ProductUpdateStatusAPIView(UpdateAPIView):
    http_method_names = ["patch"]
    permission_classes = [DjangoModelPermissions]
    product_service = ProductService()
    lookup_field = "slug"

    def get_serializer_class(self) -> Type[ModelSerializer["Product"]]:
        return ProductUpdateStatusSerializer

    def get_queryset(self) -> QuerySet["Product"]:
        return self.product_service.all()

    def partial_update(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        serialized = ProductUpdateStatusSerializer(data=request.data)  # type: ignore
        serialized.is_valid(raise_exception=True)
        instance = self.product_service.get(**kwargs)
        self.product_service.update(instance, serialized.validated_data, request=request)
        return Response({"detail": "Product Status updated."}, status=status.HTTP_200_OK)
