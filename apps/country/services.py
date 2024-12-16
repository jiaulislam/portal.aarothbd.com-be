from core.services import BaseModelService

from .models import Country


class CountryService(BaseModelService[Country]):
    model_class = Country
