from apps.user.models import User
from core.services import BaseModelService

from ..types import UserType


class UserService(BaseModelService[UserType]):
    model_class = User  # type: ignore
