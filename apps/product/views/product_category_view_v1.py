from typing import TYPE_CHECKING, Any

from django.db.models.query import QuerySet
from rest_framework import status
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateAPIView, UpdateAPIView
from rest_framework.parsers import FormParser, JSONParser, MultiPartParser
from rest_framework.permissions import DjangoModelPermissions, DjangoModelPermissionsOrAnonReadOnly
from rest_framework.response import Response

from core.request import Request

from ..serializers.product_category_serializer import ProductCategorySerializer, ProductCategoryUpdateStatusSerializer
from ..services.product_category_service import ProductCategoryService

if TYPE_CHECKING:
    from apps.product.models.product_category_model import ProductCategory


class ProductCategoryListCreateAPIView(ListCreateAPIView):
    serializer_class = ProductCategorySerializer
    permission_classes = [DjangoModelPermissionsOrAnonReadOnly]
    category_service = ProductCategoryService()
    parser_classes = [MultiPartParser, FormParser, JSONParser]

    def get_queryset(self) -> QuerySet["ProductCategory"]:
        return self.category_service.get_parent_categories()

    def list(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        parent_menus = self.category_service.get_parent_categories()
        serializer = self.get_serializer(instance=parent_menus, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = self.category_service.create(serializer.validated_data, request=request)
        serializer = self.get_serializer(instance=instance)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ProductCategoryRetrieveUpdateAPIView(RetrieveUpdateAPIView):
    http_method_names = ["get", "put"]
    serializer_class = ProductCategorySerializer
    permission_classes = [DjangoModelPermissionsOrAnonReadOnly]
    category_service = ProductCategoryService()
    lookup_field = "id"
    parser_classes = [MultiPartParser, FormParser, JSONParser]

    def get_queryset(self) -> QuerySet["ProductCategory"]:
        return self.category_service.all()

    def retrieve(self, request: Request, id: int, *args: Any, **kwargs: Any) -> Response:
        instance = self.category_service.find_by_id_or_parent_id(id)
        serializer = self.get_serializer(instance=instance)
        return Response(serializer.data)

    def update(self, request: Request, id: int, *args: Any, **kwargs: Any) -> Response:
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = self.category_service.find_by_id_or_parent_id(id)
        instance = self.category_service.update(instance, serializer.validated_data, request=request)
        serializer = self.get_serializer(instance=instance)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ProductCategoryUpdateStatusAPIView(UpdateAPIView):
    http_method_names = ["patch"]
    serializer_class = ProductCategoryUpdateStatusSerializer
    permission_classes = [DjangoModelPermissions]
    category_service = ProductCategoryService()
    lookup_field = "id"

    def get_queryset(self) -> QuerySet["ProductCategory"]:
        return self.category_service.all()

    def partial_update(self, request: Request, id: int, *args: Any, **kwargs: Any) -> Response:
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = self.category_service.find_by_id_or_parent_id(id)
        instance = self.category_service.update(instance, serializer.validated_data, request=request)
        serializer = self.get_serializer(instance=instance)
        return Response(serializer.data, status=status.HTTP_200_OK)
