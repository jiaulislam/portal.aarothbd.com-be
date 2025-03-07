from typing import TYPE_CHECKING

from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response

from core.pagination import ExtendedLimitOffsetPagination

from ..filters import ECommProductFilter
from ..serializers.product_serializer import ProductEcomSerializer, ProductNestedSerializer
from ..services import ProductService

if TYPE_CHECKING:
    pass


class EcomProductListAPIView(ListAPIView):
    serializer_class = ProductEcomSerializer
    permission_classes = [AllowAny]
    product_service = ProductService()
    pagination_class = ExtendedLimitOffsetPagination
    filterset_class = ECommProductFilter

    def get_queryset(self):
        queryset = self.product_service.get_ecom_queryset()
        filterset = self.filterset_class(self.request.GET, queryset=queryset)
        return filterset.qs.distinct()


class EcomProductDetailAPIView(RetrieveAPIView):
    serializer_class = ProductEcomSerializer
    permission_classes = [AllowAny]
    product_service = ProductService()
    lookup_field = "ecomm_identifier"

    def get_queryset(self):
        queryset = self.product_service.get_ecom_queryset()
        return queryset


class EcomCompanyProductDetailAPIView(RetrieveAPIView):
    serializer_class = ProductEcomSerializer
    permission_classes = [AllowAny]
    product_service = ProductService()

    def get_queryset(self):
        from apps.company.services import CompanyService

        company_slug = self.kwargs.get("company_slug")
        product_slug = self.kwargs.get("product_slug")
        company_service = CompanyService()
        instance = company_service.get(slug=company_slug)
        return instance.allowed_products.get(slug=product_slug)

    def retrieve(self, request: Request, *args, **kwargs) -> Response:
        instance = self.get_queryset()
        serializer = ProductNestedSerializer(instance)
        return Response(serializer.data)


class EcomCompanyProductListAPIView(ListAPIView):
    http_method_names = ["get"]
    lookup_field = "slug"
    permission_classes = [AllowAny]
    authentication_classes = []
    serializer_class = ProductEcomSerializer
    product_service = ProductService()
    pagination_class = ExtendedLimitOffsetPagination
    filterset_class = ECommProductFilter

    def get_queryset(self):
        from apps.company.services import CompanyService

        company_service = CompanyService()
        company_slug = self.kwargs.get("slug")
        company = company_service.get(slug=company_slug)
        queryset = self.product_service.get_company_product_sale_orders(company)
        filterset = self.filterset_class(self.request.GET, queryset=queryset)
        return filterset.qs.distinct()

    def list(self, request: Request, *args, **kwargs) -> Response:
        queryset = self.get_queryset()
        page = self.pagination_class()  # type: ignore
        paginate_queryset = page.paginate_queryset(queryset, request)
        serializer = self.get_serializer(paginate_queryset, many=True)
        return page.get_paginated_response(serializer.data)
