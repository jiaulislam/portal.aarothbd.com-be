from typing import TYPE_CHECKING

from django.db.models.query import QuerySet
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response

from core.pagination import ExtendedLimitOffsetPagination

from ..serializers.product_serializer import ProductEcomSerializer, ProductNestedSerializer
from ..services import ProductService

if TYPE_CHECKING:
    from apps.product.models.product_model import Product


class EcomProductListAPIView(ListAPIView):
    serializer_class = ProductEcomSerializer
    permission_classes = [AllowAny]
    product_service = ProductService()
    pagination_class = ExtendedLimitOffsetPagination

    def get_queryset(self):
        queryset = self.product_service.get_ecom_queryset()
        return queryset


class EcomProductDetailAPIView(RetrieveAPIView):
    serializer_class = ProductEcomSerializer
    permission_classes = [AllowAny]
    product_service = ProductService()
    lookup_field = "ecomm_identifier"

    def get_queryset(self):
        queryset = self.product_service.get_ecom_queryset()
        return queryset


class EcomCompanyProductListAPIView(ListAPIView):
    http_method_names = ["get"]
    lookup_field = "slug"
    permission_classes = [AllowAny]
    authentication_classes = []
    serializer_class = ProductNestedSerializer
    product_service = ProductService()
    pagination_class = ExtendedLimitOffsetPagination

    def get_queryset(self, company_slug: str) -> QuerySet["Product"]:
        from apps.company.services import CompanyService

        company_service = CompanyService()
        instance = company_service.get(slug=company_slug)
        return instance.allowed_products.all()

    def list(self, request: Request, slug: str, *args, **kwargs) -> Response:
        queryset = self.get_queryset(company_slug=slug)
        page = self.pagination_class()  # type: ignore
        paginate_queryset = page.paginate_queryset(queryset, request)
        serializer = ProductNestedSerializer(paginate_queryset, many=True)
        return page.get_paginated_response(serializer.data)
