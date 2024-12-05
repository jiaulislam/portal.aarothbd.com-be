from datetime import datetime
from typing import NotRequired, TypedDict, TypeVar

from django.contrib.auth.models import AbstractBaseUser
from django.db.models import Model

__all__ = ["_T", "BaseSerializerValidatedDataType"]

_T = TypeVar("_T", bound=Model)


class BaseSerializerValidatedDataType(TypedDict):
    is_active: bool
    created_at: NotRequired[datetime] | None
    updated_at: NotRequired[datetime] | None
    created_by: NotRequired[AbstractBaseUser] | None
    updated_by: NotRequired[AbstractBaseUser] | None
