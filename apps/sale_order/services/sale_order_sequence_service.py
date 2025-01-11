from core.services import BaseModelService

from ..models import SaleOrderSequence


class SaleOrderSequenceService(BaseModelService):
    model_class = SaleOrderSequence
