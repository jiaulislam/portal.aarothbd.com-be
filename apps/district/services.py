from core.services import BaseModelService

from .models import District


class DistrictService(BaseModelService):
    model_class = District
