from typing import Any

from rest_framework import status
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateAPIView, UpdateAPIView
from rest_framework.permissions import DjangoModelPermissions
from rest_framework.response import Response

from core.request import Request

from ..serializers.product_category_serializer import ProductCategorySerializer, ProductCategoryUpdateStatusSerializer
from ..services.product_category_service import ProductCategoryService


class ProductCategoryListCreateAPIView(ListCreateAPIView):
    serializer_class = ProductCategorySerializer
    permission_classes = [DjangoModelPermissions]
    category_service = ProductCategoryService()

    def create(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        serializer = ProductCategorySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = self.category_service.create(serializer.validated_data, request=request)
        serializer = ProductCategorySerializer(instance=instance)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ProductCategoryRetrieveUpdateAPIView(RetrieveUpdateAPIView):
    http_method_names = ["get", "put"]
    serializer_class = ProductCategorySerializer
    permission_classes = [DjangoModelPermissions]
    category_service = ProductCategoryService()

    def update(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        serializer = ProductCategorySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = self.category_service.get(**kwargs)
        instance = self.category_service.update(instance, serializer.validated_data, request=request)
        serializer = ProductCategorySerializer(instance=instance)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ProductCategoryUpdateStatusAPIView(UpdateAPIView):
    http_method_names = ["patch"]
    serializer_class = ProductCategorySerializer
    permission_classes = [DjangoModelPermissions]
    category_service = ProductCategoryService()

    def partial_update(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        serializer = ProductCategoryUpdateStatusSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = self.category_service.get(**kwargs)
        instance = self.category_service.update(instance, serializer.validated_data, request=request)
        serializer = ProductCategoryUpdateStatusSerializer(instance=instance)
        return Response(serializer.data, status=status.HTTP_200_OK)
