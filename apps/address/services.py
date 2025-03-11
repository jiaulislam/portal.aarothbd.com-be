from typing import Union
from uuid import UUID

from django.contrib.admin.options import get_content_type_for_model
from django.contrib.contenttypes.models import ContentType

from core.services import BaseModelService

from ..company.models import Company
from .models import Address

ID_TYPE = Union[str, int, UUID, None]


class AddressService(BaseModelService[Address]):
    model_class = Address

    def prepare_data(self, validated_data, *args, **kwargs):
        return validated_data

    def create_address(self, company_data, /, content_type: ContentType, object_id: ID_TYPE, **kwargs):
        validated_data = self.prepare_data(company_data, **kwargs)
        return Address(content_type=content_type, object_id=object_id, **validated_data)

    def create_company_addresses(self, validated_data_list, company: Company, **kwargs):
        addresses = []
        content_type = get_content_type_for_model(company)
        for company_data in validated_data_list:
            object_id = company.id  # type: ignore
            address = self.create_address(company_data, content_type=content_type, object_id=object_id, **kwargs)
            addresses.append(address)
        return Address.objects.bulk_create(addresses)

    def create_user_addresses(self, validated_data_list, user, **kwargs):
        addresses = []
        content_type = get_content_type_for_model(user)
        for user_data in validated_data_list:
            object_id = user.id
            address = self.create_address(user_data, content_type=content_type, object_id=object_id, **kwargs)
            addresses.append(address)
        return Address.objects.bulk_create(addresses)

    def create_user_address(self, validated_data, user, **kwargs):
        request = kwargs.get("request")
        content_type = get_content_type_for_model(user)
        object_id = user.id
        validated_data["content_type"] = content_type
        validated_data["object_id"] = object_id
        address = self.create(validated_data, request=request)
        return address

    def update_status(self, instance: Address, status: bool, *args, **kwargs):
        instance.is_active = status
        instance.updated_by = self.core_service.get_user(kwargs["request"])  # type: ignore
        instance.save()
        return instance
