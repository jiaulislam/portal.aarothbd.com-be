from core.services import BaseModelService

from ..models import CompanyConfiguration

__all__ = ["CompanyConfigurationService"]


class CompanyConfigurationService(BaseModelService[CompanyConfiguration]):
    model_class = CompanyConfiguration
