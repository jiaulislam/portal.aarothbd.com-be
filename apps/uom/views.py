from typing import Any

from django.db.models.query import QuerySet
from rest_framework import status
from rest_framework.generics import ListCreateAPIView
from rest_framework.permissions import DjangoModelPermissions
from rest_framework.response import Response

from core.pagination import ExtendedLimitOffsetPagination
from core.request import Request

from .filters import UoMCategoryFilter, UoMFilter
from .models import UoM, UoMCategory
from .serializers import UoMCategorySerializer, UoMCreateSerializer, UoMSerializer


class UoMCategoryListCreateAPIView(ListCreateAPIView):
    serializer_class = UoMCategorySerializer
    queryset = UoMCategory.objects.all()
    permission_classes = [DjangoModelPermissions]
    filterset_class = UoMCategoryFilter
    pagination_class = ExtendedLimitOffsetPagination


class UoMListCreateAPIView(ListCreateAPIView):
    serializer_class = UoMSerializer
    permission_classes = [DjangoModelPermissions]
    filterset_class = UoMFilter
    pagination_class = ExtendedLimitOffsetPagination

    def get_queryset(self) -> QuerySet["UoM"]:
        queryset = UoM.objects.all()
        filterset = self.filterset_class(self.request.GET, queryset=queryset)
        return filterset.qs

    def create(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        serializer = UoMCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
