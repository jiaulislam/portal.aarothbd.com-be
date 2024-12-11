from core.services import BaseModelService

from .models import Division


class DivisionService(BaseModelService):
    model_class = Division
