from core.services import BaseModelService

from .models import Action


class ActionService(BaseModelService[Action]):
    model_class = Action
