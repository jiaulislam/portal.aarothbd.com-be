from core.services import BaseModelService

from .models import Action


class ActionService(BaseModelService):
    model_class = Action
