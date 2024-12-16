from core.services import BaseModelService

from .models import Division


class DivisionService(BaseModelService[Division]):
    model_class = Division
