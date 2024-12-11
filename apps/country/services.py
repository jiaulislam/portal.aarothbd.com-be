from core.services import BaseModelService

from .models import Country


class CountryService(BaseModelService):
    model_class = Country
