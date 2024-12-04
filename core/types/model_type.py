from datetime import datetime
from typing import NotRequired, TypedDict, TypeVar

from django.contrib.auth.models import AbstractBaseUser
from django.db.models import Model

__all__ = ["_T", "SerializedValidatedDataType"]

_T = TypeVar("_T", bound=Model)


class MutableBaseSerializerValidatedData(TypedDict):
    is_active: bool
    created_at: NotRequired[datetime] | None
    updated_at: NotRequired[datetime] | None
    created_by: NotRequired[AbstractBaseUser] | None
    updated_by: NotRequired[AbstractBaseUser] | None


SerializedValidatedDataType = MutableBaseSerializerValidatedData
