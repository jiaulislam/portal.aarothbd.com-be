import secrets
import string
from typing import Any, MutableMapping, Tuple

from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import Permission
from django.forms import model_to_dict

from core.constants.common import AUDIT_COLUMNS
from core.exceptions import CustomException
from core.services import BaseModelService

from ..constants import UserTypeChoices
from ..types import UserType

User = get_user_model()


class UserService(BaseModelService[UserType]):
    model_class = User  # type: ignore
    company_required_user_type = [UserTypeChoices.WHOLESELLER_ADMIN]

    def validate_wholeseller_has_company(self, validated_data: MutableMapping[str, Any]) -> bool:
        user_type = validated_data.get("user_type", None)
        if user_type not in self.company_required_user_type:
            return True  # no need this validation for other types of user
        return bool(validated_data.get("company", None))

    def hash_password(self, plain_text_password: str) -> str:
        if not bool(plain_text_password):
            raise CustomException(detail="password field cannot be empty!")
        return make_password(plain_text_password)

    def create(self, validated_data: MutableMapping[str, Any], **kwargs) -> UserType:
        if not self.validate_wholeseller_has_company(validated_data):
            raise CustomException(detail=f"Company required for user type {validated_data.get('user_type')}!")

        password2 = validated_data.pop("password2", "")
        profile = validated_data.pop("profile", {})
        validated_data["password"] = self.hash_password(password2)
        validated_data["created_by"] = self.core_service.get_user(kwargs.get("request"))
        instance = self.model_class.objects.create(**validated_data)
        self.update_user_profile(instance, profile)
        return instance

    def create_customer(self, validated_data: MutableMapping[str, Any], **kwargs) -> UserType:
        validated_data["user_type"] = "customer"
        validated_data["is_active"] = False
        instance = self.create(validated_data, **kwargs)
        return instance

    def update_user_profile(self, user: UserType, profile_data: MutableMapping[str, Any]):
        profile = user.profile
        for attr, value in profile_data.items():
            setattr(profile, attr, value)
        user.profile.save()

    def update(self, instance: UserType, validated_data: MutableMapping[str, Any], **kwargs) -> UserType:
        profile_data = validated_data.pop("profile", {})
        if profile_data:
            self.update_user_profile(instance, profile_data)
        return super().update(instance, validated_data, **kwargs)

    def get_users_permissions_groups(self, user):
        permission_id_list = []
        group_list = []
        if hasattr(user, "groups"):
            for group in user.groups.all():
                permission_id_list += group.permissions.values_list("id", flat=True)
                group_list.append(model_to_dict(group, fields="id, name"))

        permissions = Permission.objects.filter(id__in=set(permission_id_list))
        permissions = permissions.values("id", "name", "content_type_id", "codename") if permissions else []

        user = model_to_dict(user, exclude="groups, password, user_permissions")
        user["groups"] = group_list
        user["permissions"] = permissions

        return user

    @staticmethod
    def generate_random_password(length=10):
        """Generate a secure random password using the secrets module."""
        if length < 8:
            raise ValueError("Password length should be at least 8 characters for security.")

        # Ensure at least one uppercase letter and one digit
        uppercase = secrets.choice(string.ascii_uppercase)
        digit = secrets.choice(string.digits)

        # Fill the rest with a mix of letters, digits, and punctuation
        all_chars = string.ascii_letters + string.digits + string.punctuation
        remaining_chars = "".join(secrets.choice(all_chars) for _ in range(length - 2))

        # Shuffle to avoid predictable patterns
        password = list(uppercase + digit + remaining_chars)
        secrets.SystemRandom().shuffle(password)

        return "".join(password)

    def get_or_create_social_auth_user(
        self, validated_data: MutableMapping[str, Any], *args, **kwargs
    ) -> Tuple[UserType, bool]:
        user = self.model_class.objects.filter(
            email=validated_data.get("email"),
        ).first()
        if user:
            return user, False
        validated_data["user_type"] = "customer"
        validated_data["password2"] = self.generate_random_password()
        validated_data["is_active"] = True  # as user is already coming from social email. already email validated
        instance = self.create(validated_data, **kwargs)
        return instance, True

    def change_password(self, user: UserType, password: str) -> UserType:
        user.set_password(password)
        user.save()
        return user

    def get_user_addresses(self, user: UserType):
        data = [model_to_dict(address, exclude=AUDIT_COLUMNS) for address in user.addresses.all()]
        return data
