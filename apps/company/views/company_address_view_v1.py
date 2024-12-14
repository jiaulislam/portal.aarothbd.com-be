from rest_framework import status
from rest_framework.generics import ListCreateAPIView
from rest_framework.response import Response

from apps.address.serializers import AddressSerializer
from apps.address.services import AddressService

from ..services import CompanyService


class CompanyAddressListCreateAPIView(ListCreateAPIView):
    serializer_class = AddressSerializer
    address_service = AddressService()
    company_service = CompanyService()

    def get_queryset(self):
        return self.address_service.all()

    def list(self, request, *args, **kwargs):
        company_id = kwargs.get('company_id')
        company = self.company_service.get(id=company_id)
        addresses = company.addresses.all()
        serialized = self.serializer_class(addresses, many=True)
        return Response(serialized.data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        company_id = kwargs.get("company_id")
        company = self.company_service.get(id=company_id)
        serialized = self.serializer_class(data=request.data)
        serialized.is_valid(raise_exception=True)
        instance = self.address_service.create_address(serialized.validated_data, company, request=request)
        instance.save()
        serialized = self.serializer_class(instance=instance)
        return Response(serialized.data, status=status.HTTP_201_CREATED)
