from django.contrib.auth.models import Permission

from core.services.base_model_service import BaseModelService

__all__ = ["PermissionService"]


class PermissionService(BaseModelService):
    model_class = Permission
