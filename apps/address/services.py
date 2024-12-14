from typing import List

from django.contrib.admin.options import get_content_type_for_model

from core.services import BaseModelService

from ..company.models import Company
from .models import Address
from .types import AddressValidatedDataType


class AddressService(BaseModelService):
    model_class = Address

    def prepare_data(self, validated_data: AddressValidatedDataType, *args, **kwargs):
        return validated_data

    def create_address(self, company_data: AddressValidatedDataType, company: Company, *args, **kwargs):
        content_type = get_content_type_for_model(company)
        validated_data = self.prepare_data(company_data, *args, **kwargs)
        return Address(content_type=content_type, object_id=company.id, **validated_data)

    def create_company_addresses(
        self, validated_data_list: List[AddressValidatedDataType], company: Company, *args, **kwargs
    ):
        addresses = []
        for company_data in validated_data_list:
            address = self.create_address(company_data, company, *args, **kwargs)
            addresses.append(address)
        return Address.objects.bulk_create(addresses)

    def update_status(self, instance: Address, status: bool, *args, **kwargs):
        instance.is_active = status
        instance.updated_by = self.core_service.get_user(kwargs["request"])
        instance.save()
        return instance
