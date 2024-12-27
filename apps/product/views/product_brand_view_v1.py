from typing import TYPE_CHECKING, Any

from django.db.models.query import QuerySet
from rest_framework import status
from rest_framework.generics import ListCreateAPIView
from rest_framework.permissions import DjangoModelPermissions
from rest_framework.response import Response

from core.pagination import ExtendedLimitOffsetPagination
from core.request import Request

from ..serializers.product_brand_serializer import ProductBrandSerializer
from ..services.product_brand_service import ProductBrandService

if TYPE_CHECKING:
    from apps.product.models.product_brand_model import ProductBrand


class ProductBrandListCreateAPIView(ListCreateAPIView):
    serializer_class = ProductBrandSerializer
    permission_classes = [DjangoModelPermissions]
    brand_service = ProductBrandService()
    pagination_class = ExtendedLimitOffsetPagination

    def get_queryset(self) -> QuerySet["ProductBrand"]:
        return self.brand_service.all()

    def create(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        serializer = ProductBrandSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = self.brand_service.create(serializer.validated_data, request=request)
        serializer = ProductBrandSerializer(instance=instance)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
