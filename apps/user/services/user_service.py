from typing import Any, MutableMapping

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
            raise CustomException(detail=f"Company required for user type {validated_data.get("user_type")}!")

        password2 = validated_data.pop("password2", "")
        validated_data["password"] = self.hash_password(password2)
        validated_data["created_by"] = self.core_service.get_user(kwargs.get("request"))
        instance = self.model_class.objects.create(**validated_data)
        return instance

    def create_customer(self, validated_data: UserValidatedDataType, **kwargs) -> UserType:
        validated_data["user_type"] = "customer"
        validated_data["is_active"] = False
        instance = self.create(validated_data, **kwargs)
        return instance

    def update_user_profile(self, user: UserType, profile_data: MutableMapping[str, Any]):
        profile = user.profile
        for attr, value in profile_data.items():
            setattr(profile, attr, value)
        user.profile.save()

    def update(self, instance: UserType, validated_data: UserValidatedDataType, **kwargs) -> UserType:
        profile_data = validated_data.pop("profile")
        self.update_user_profile(instance, profile_data)
        return super().update(instance, validated_data, **kwargs)
