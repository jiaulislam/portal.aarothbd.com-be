from django.db.models.query import QuerySet
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.permissions import AllowAny

from core.pagination import ExtendedLimitOffsetPagination

from ..serializers.product_serializer import ProductEcomSerializer, ProductExtendedSerializer
from ..services import ProductService


class EcomProductListAPIView(ListAPIView):
    serializer_class = ProductEcomSerializer
    permission_classes = [AllowAny]
    product_service = ProductService()
    pagination_class = ExtendedLimitOffsetPagination

    def get_queryset(self):
        queryset = self.product_service.get_ecom_queryset()
        return queryset


class EcomProductDetailAPIView(RetrieveAPIView):
    serializer_class = ProductExtendedSerializer
    permission_classes = [AllowAny]
    product_service = ProductService()
    lookup_field = "slug"

    def get_queryset(self) -> QuerySet:
        queryset = self.product_service.all()
        return queryset
