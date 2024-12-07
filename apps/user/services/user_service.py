from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password

from core.exceptions import CustomException
from core.services import BaseModelService

from ..constants import UserTypeChoices
from ..types import UserType, UserValidatedDataType

User = get_user_model()


class UserService(BaseModelService[UserType]):
    model_class = User  # type: ignore
    company_required_user_type = [UserTypeChoices.WHOLESELLER_ADMIN]

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

    def validate_wholeseller_has_company(self, validated_data: UserValidatedDataType) -> bool:
        user_type = validated_data.get("user_type", None)
        if user_type not in self.company_required_user_type:
            return True  # no need this validation for other types of user
        return bool(validated_data.get("company", None))

    def hash_password(self, plain_text_password: str) -> str:
        if not bool(plain_text_password):
            raise CustomException(detail="password field cannot be empty!")
        return make_password(plain_text_password)

    def create(self, validated_data: UserValidatedDataType, **kwargs) -> UserType:
        if not self.validate_wholeseller_has_company(validated_data):
            raise CustomException(detail=f"Company required for {UserTypeChoices.WHOLESELLER_ADMIN.label!r} user type!")
        validated_data["created_by"] = self.core_service.get_user(kwargs.get("request"))
        instance = self.model_class.objects.create(**validated_data)
        return instance

    def create_customer(self, validated_data: UserValidatedDataType, **kwargs) -> UserType:
        validated_data["user_type"] = "customer"
        validated_data["is_active"] = False
        instance = self.create(validated_data, **kwargs)
        return instance
