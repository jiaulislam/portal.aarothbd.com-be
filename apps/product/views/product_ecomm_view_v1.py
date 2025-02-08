from rest_framework.generics import ListAPIView
from rest_framework.permissions import AllowAny

from core.pagination import ExtendedLimitOffsetPagination

from ..serializers.product_serializer import ProductEcomSerializer
from ..services import ProductService


class EcomProductListAPIView(ListAPIView):
    serializer_class = ProductEcomSerializer
    permission_classes = [AllowAny]
    product_service = ProductService()
    pagination_class = ExtendedLimitOffsetPagination

    def get_queryset(self):
        queryset = self.product_service.get_ecom_queryset()
        return queryset
