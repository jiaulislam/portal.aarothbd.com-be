from django.contrib.auth import get_user_model

from core.services import BaseModelService

User = get_user_model()


class UserService(BaseModelService[User]):
    model_class = User  # type: ignore
