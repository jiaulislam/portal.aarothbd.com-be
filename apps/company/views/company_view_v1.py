from django.db import transaction
from django.db.models import QuerySet
from rest_framework import status
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateAPIView, UpdateAPIView
from rest_framework.request import Request
from rest_framework.response import Response

from core.pagination import ExtendedLimitOffsetPagination

from ..filters import CompanyFilter
from ..models import Company
from ..serializers.company_configuration_serializer_v1 import CompanyConfigurationSerializer
from ..serializers.company_serializer_v1 import CompanySerializer, CompanyUpdateStatusSerializer
from ..services import CompanyConfigurationService, CompanyService


class CompanyListCreateAPIView(ListCreateAPIView):
    serializer_class = CompanySerializer
    filterset_class = CompanyFilter
    pagination_class = ExtendedLimitOffsetPagination

    company_service = CompanyService()
    company_configuration_service = CompanyConfigurationService()

    def get_queryset(self, **kwargs) -> QuerySet[Company]:
        queryset = self.company_service.all(**kwargs).select_related("configuration")
        filterset = self.filterset_class(self.request.GET, queryset=queryset)
        return filterset.qs

    def list(self, request: Request, *args, **kwargs) -> Response:
        queryset = self.get_queryset(**kwargs)
        paginate = self.pagination_class()  # type: ignore
        paginated_queryset = paginate.paginate_queryset(queryset, request)
        serialized = self.serializer_class(paginated_queryset, many=True)  # type: ignore
        return paginate.get_paginated_response(serialized.data)

    @transaction.atomic
    def create(self, request: Request, *args, **kwargs) -> Response:
        configuration_data = request.data.get("configuration", {})
        serialized = self.serializer_class(data=request.data)  # type: ignore
        serialized.is_valid(raise_exception=True)
        instance = self.company_service.create(serialized.data, request=request)
        configuration_data["company"] = instance.id
        configuration_serialized = CompanyConfigurationSerializer(data=configuration_data)
        configuration_serialized.is_valid(raise_exception=True)
        self.company_configuration_service.create(configuration_serialized.validated_data, request=request)
        serialized = self.serializer_class(instance=instance)  # type: ignore
        return Response(serialized.data, status=status.HTTP_201_CREATED)


class CompanyRetrieveUpdateAPIView(RetrieveUpdateAPIView):
    http_method_names = ["get", "put"]
    serializer_class = CompanySerializer

    company_service = CompanyService()
    company_configuration_service = CompanyConfigurationService()

    def retrieve(self, request: Request, *args, **kwargs) -> Response:
        _company_id = kwargs.get("id")
        queryset = self.company_service.get(id=_company_id, select_related=["configuration"])
        serialized = self.serializer_class(queryset)  # type: ignore
        return Response(serialized.data, status=status.HTTP_200_OK)

    @transaction.atomic
    def update(self, request: Request, *args, **kwargs):
        _company_id = kwargs.get("id")
        configuration_data = request.data.get("configuration", {})
        configuration_serialized = CompanyConfigurationSerializer(data=configuration_data)
        configuration_serialized.is_valid(raise_exception=True)
        configuration_id = configuration_serialized.validated_data.pop("id")

        company_serialized = self.serializer_class(data=request.data)  # type: ignore
        company_serialized.is_valid(raise_exception=True)
        # get and update configuration
        configuration_instance = self.company_configuration_service.get(id=configuration_id)
        _ = self.company_configuration_service.update(
            configuration_instance,
            configuration_serialized.validated_data,
            request=request,
        )

        # get and update company
        company_instance = self.company_service.get(id=_company_id)
        _ = self.company_service.update(
            company_instance,
            company_serialized.validated_data,
            request=request,
        )

        response_data = {"detail": "Company Updated successfully."}
        return Response(response_data, status=status.HTTP_200_OK)


class CompanyUpdateStatusAPIView(UpdateAPIView):
    http_method_names = ["patch"]
    serializer_class = CompanyUpdateStatusSerializer

    company_service = CompanyService()

    def partial_update(self, request: Request, *args, **kwargs):
        serialized = self.serializer_class(data=request.data)  # type: ignore
        serialized.is_valid(raise_exception=True)
        _company_id = kwargs.get("id")
        instance = self.company_service.get(id=_company_id)
        self.company_service.update(instance, serialized.validated_data, request=request)
        return Response({"detail": "Company Status updated."}, status=status.HTTP_200_OK)
