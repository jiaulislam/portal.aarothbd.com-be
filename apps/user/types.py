from datetime import datetime
from typing import Literal

from django.contrib.auth import get_user_model

from core.types import SerializedValidatedDataType

from .models import User

AbstractUserModel = get_user_model()

UserType = User

UserCategory = Literal["central_admin"] | Literal["customer"] | Literal["wholeseller"]


class UserValidatedDataType(SerializedValidatedDataType):
    email: str
    first_name: str | None
    last_name: str | None
    is_admin: bool
    date_joined: datetime | None
    user_type: UserCategory
    password: str
    last_login: datetime | None
