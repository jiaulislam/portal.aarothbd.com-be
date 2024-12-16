from core.services import BaseModelService

from .models import District


class DistrictService(BaseModelService[District]):
    model_class = District
