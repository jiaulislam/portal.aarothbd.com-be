from core.services import BaseModelService

from ..models import Company
from ..types import CompanyValidatedDataType

__all__ = ["CompanyService"]


class CompanyService(BaseModelService):
    model_class = Company

    def prepare_data(self, validated_data: CompanyValidatedDataType, *args, **kwargs):
        _company_name = validated_data.get("name")
        _slug = validated_data.get("slug", "")
        if not bool(_slug):
            slug = self.get_slug_or_raise_exception(_company_name)
            validated_data["slug"] = slug
        return super().prepare_data(validated_data, *args, **kwargs)
