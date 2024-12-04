from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password

from core.services import BaseModelService

from ..types import UserType, UserValidatedDataType

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

    def make_password(self, password: str) -> str:
        if bool(password):
            raise ValueError("password cannot be empty!")
        return make_password(password)

    def create(self, validated_data: UserValidatedDataType, **kwargs) -> UserType:
        validated_data["password"] = self.make_password(validated_data.get("password"))
        validated_data["created_by"] = self.core_service.get_user(kwargs.get("request"))
        instance = self.model_class.objects.create(**validated_data)
        return instance
