from typing import Any

from rest_framework import status
from rest_framework.generics import ListCreateAPIView
from rest_framework.permissions import DjangoModelPermissions
from rest_framework.response import Response

from core.request import Request

from ..serializers.product_brand_serializer import ProductBrandSerializer
from ..services.product_brand_service import ProductBrandService


class ProductBrandListCreateAPIView(ListCreateAPIView):
    serializer_class = ProductBrandSerializer
    permission_classes = [DjangoModelPermissions]
    brand_service = ProductBrandService()

    def create(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        serializer = ProductBrandSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = self.brand_service.create(serializer.validated_data, request=request)
        serializer = ProductBrandSerializer(instance=instance)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
