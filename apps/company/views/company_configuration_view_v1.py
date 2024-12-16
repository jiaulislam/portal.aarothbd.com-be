from rest_framework import status
from rest_framework.generics import UpdateAPIView
from rest_framework.response import Response

from ..serializers.company_configuration_serializer_v1 import CompanyConfigurationCreateSerializer
from ..services import CompanyConfigurationService, CompanyService


class CompanyConfigurationUpdateAPIView(UpdateAPIView):
    http_method_names = ["put"]
    serializer_class = CompanyConfigurationCreateSerializer
    configuration_service = CompanyConfigurationService()
    company_service = CompanyService()

    def get_queryset(self):
        return self.configuration_service.all()

    def update(self, request, *args, **kwargs):
        company_id = kwargs.get("company_id")
        company = self.company_service.get(id=company_id)
        serialized = CompanyConfigurationCreateSerializer(data=request.data)
        serialized.is_valid(raise_exception=True)
        instance = self.configuration_service.update(company.configuration, serialized.validated_data, request=request)
        serialized = CompanyConfigurationCreateSerializer(instance=instance)
        return Response(serialized.data, status=status.HTTP_201_CREATED)
