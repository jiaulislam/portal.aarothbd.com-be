from core.services import BaseModelService

from .models import UoM, UoMCategory


class UomCategoryService(BaseModelService):
    model_class = UoMCategory


class UomService(BaseModelService):
    model_class = UoM
