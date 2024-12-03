from django.contrib.auth.models import Group

from core.services.base_model_service import BaseModelService

__all__ = ["GroupService"]


class GroupService(BaseModelService):
    model_class = Group
