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

    def hash_password(self, plain_text_password: str) -> str:
        if bool(plain_text_password):
            raise ValueError("password field cannot be empty!")
        return make_password(plain_text_password)

    def create(self, validated_data: UserValidatedDataType, **kwargs) -> UserType:
        validated_data["created_by"] = self.core_service.get_user(kwargs.get("request"))
        instance = self.model_class.objects.create(**validated_data)
        return instance

    def create_customer(self, validated_data: UserValidatedDataType, **kwargs) -> UserType:
        validated_data["user_type"] = "customer"
        validated_data["is_active"] = False
        instance = self.create(validated_data, **kwargs)
        return instance
