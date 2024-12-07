from django.db import transaction
from django.db.models import QuerySet
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.request import Request
from rest_framework.response import Response

from core.pagination import ExtendedLimitOffsetPagination

from ..filters import CompanyFilter
from ..models import Company
from ..serializers.company_configuration_serializer_v1 import CompanyConfigurationSerializer
from ..serializers.company_serializer_v1 import CompanySerializer, CompanyUpdateStatusSerializer
from ..services import CompanyConfigurationService, CompanyService


class CompanyListCreateAPIView(GenericAPIView):
    serializer_class = CompanySerializer
    filterset_class = CompanyFilter
    pagination_class = ExtendedLimitOffsetPagination

    company_service = CompanyService()
    company_configuration_service = CompanyConfigurationService()

    def get_queryset(self, **kwargs) -> QuerySet[Company]:
        queryset = self.company_service.all(**kwargs)
        filterset = self.filterset_class(self.request.GET, queryset=queryset)
        return filterset.qs

    def get(self, request: Request, *args, **kwargs) -> Response:
        queryset = self.get_queryset(**kwargs)
        paginate = self.pagination_class()  # type: ignore
        paginated_queryset = paginate.paginate_queryset(queryset, request)
        serialized = self.serializer_class(paginated_queryset, many=True)  # type: ignore
        return paginate.get_paginated_response(serialized.data)

    @transaction.atomic
    def post(self, request: Request, *args, **kwargs) -> Response:
        company_data = request.data.get("configuration", {})
        serialized = self.serializer_class(data=request.data)  # type: ignore
        serialized.is_valid(raise_exception=True)
        instance = self.company_service.create(serialized.data, request=request)
        company_data["company"] = instance.id
        configuration_serialized = CompanyConfigurationSerializer(data=company_data)
        configuration_serialized.is_valid(raise_exception=True)
        self.company_configuration_service.create(configuration_serialized.validated_data, request=request)
        serialized = self.serializer_class(instance=instance)  # type: ignore
        return Response(serialized.data, status=status.HTTP_201_CREATED)


class CompanyRetrieveUpdateAPIView(GenericAPIView):
    serializer_class = CompanySerializer

    company_service = CompanyService()

    def get(self, request: Request, id: int, **kwargs) -> Response:
        queryset = self.company_service.get(id=id)
        serialized = self.serializer_class(queryset)  # type: ignore
        return Response(serialized.data, status=status.HTTP_200_OK)

    def post(self, request: Request, id: int, **kwargs):
        serialized = self.serializer_class(data=request.data)  # type: ignore
        serialized.is_valid(raise_exception=True)
        instance = self.company_service.get(id=id)
        instance = self.company_service.update(instance, serialized.validated_data, request=request)
        response_data = {"detail": "Company Updated successfully."}
        return Response(response_data, status=status.HTTP_200_OK)


class CompanyUpdateStatusAPIView(GenericAPIView):
    serializer_class = CompanyUpdateStatusSerializer

    company_service = CompanyService()

    def post(self, request: Request, id: int, **kwargs):
        serialized = self.serializer_class(data=request.data)  # type: ignore
        serialized.is_valid(raise_exception=True)
        instance = self.company_service.get(id=id)
        self.company_service.update(instance, serialized.data, request=request)
        return Response({"detail": "Company Status updated."}, status=status.HTTP_200_OK)
