from django.contrib.auth import get_user_model

from core.services import BaseModelService

from ..types import UserType

User = get_user_model()


class UserService(BaseModelService[UserType]):
    model_class = User  # type: ignore

    def all(self, **kwargs):
        return (
            super()
            .all(**kwargs)
            .select_related("profile")
            .prefetch_related(
                "groups",
                "user_permissions",
            )
        )
