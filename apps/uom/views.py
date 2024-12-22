from typing import Any

from rest_framework import status
from rest_framework.generics import ListCreateAPIView
from rest_framework.permissions import DjangoModelPermissions
from rest_framework.response import Response

from core.request import Request

from .models import UoM, UoMCategory
from .serializers import UoMCategorySerializer, UoMCreateSerializer, UoMSerializer


class UoMCategoryListCreateAPIView(ListCreateAPIView):
    serializer_class = UoMCategorySerializer
    queryset = UoMCategory.objects.all()
    permission_classes = [DjangoModelPermissions]


class UoMListCreateAPIView(ListCreateAPIView):
    serializer_class = UoMSerializer
    queryset = UoM.objects.all()
    permission_classes = [DjangoModelPermissions]

    def get(self, request: Request, *args, **kwargs):
        serializer = UoMSerializer(instance=self.queryset.all(), many=True)  # type: ignore
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        serializer = UoMCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
