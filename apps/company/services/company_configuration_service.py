from core.services import BaseModelService

from ..models import CompanyConfiguration

__all__ = ["CompanyConfigurationService"]


class CompanyConfigurationService(BaseModelService):
    model_class = CompanyConfiguration
