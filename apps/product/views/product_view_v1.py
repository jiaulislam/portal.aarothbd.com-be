from typing import Any, MutableMapping

from django.db import transaction
from rest_framework import status
from rest_framework.generics import ListCreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response

from ..serializers.product_serializer import ProductCreateSerializer
from ..services import ProductBrandService, ProductService


class ProductListCreateAPIView(ListCreateAPIView):
    serializer_class = ProductCreateSerializer
    permission_classes = [IsAuthenticated]
    product_service = ProductService()
    brand_service = ProductBrandService()

    @transaction.atomic
    def create(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        serialized = self.serializer_class(data=request.data)  # type: ignore
        serialized.is_valid(raise_exception=True)

        brand: MutableMapping[str, Any] = serialized.validated_data.pop("brand", {})
        if brand:
            _brand, _ = self.brand_service.get_or_create(brand, request=request)
            serialized.validated_data["brand"] = _brand

        instance = self.product_service.create(serialized.validated_data, request=request)
        serialized = self.serializer_class(instance=instance)  # type: ignore

        return Response(serialized.data, status=status.HTTP_200_OK)
