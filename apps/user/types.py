from datetime import datetime
from typing import Literal

from django.contrib.auth import get_user_model

from apps.company.types import CompanyValidatedDataType
from core.types import BaseSerializerValidatedDataType

from .models import User

AbstractUserModel = get_user_model()

UserType = User

UserCategory = Literal["central_admin"] | Literal["customer"] | Literal["wholeseller"]


class UserValidatedDataType(BaseSerializerValidatedDataType):
    email: str
    first_name: str | None
    last_name: str | None
    is_admin: bool
    date_joined: datetime | None
    user_type: UserCategory
    password: str
    last_login: datetime | None
    company: CompanyValidatedDataType | None
