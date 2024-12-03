from datetime import datetime
from typing import TypedDict

from django.contrib.auth import get_user_model

from .models import User

AbstractUserModel = get_user_model()

UserType = AbstractUserModel | User


class TokenResponse(TypedDict):
    refresh_token: str
    access_token: str
    iat: str
    exp: int


class UserValidatedDataType(TypedDict):
    email: str
    first_name: str | None
    last_name: str | None
    is_admin: bool
    is_active: bool
    created_at: datetime | None
    updated_at: datetime | None
    created_by: User | None
    updated_by: User | None
