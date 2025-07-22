from typing import Any, MutableMapping

from core.services import BaseModelService

from ..models import Company

__all__ = ["CompanyService"]


class CompanyService(BaseModelService[Company]):
    model_class = Company

    def prepare_data(self, validated_data: MutableMapping[str, Any], *args, **kwargs):
        _company_name = validated_data.get("name")
        validated_data["slug"] = self.get_slug_or_raise_exception(_company_name)
        return super().prepare_data(validated_data, *args, **kwargs)
