from typing import MutableMapping, TypedDict, TypeVar, Union

from django.db.models import Manager, Model

__all__ = ["DjangoModel", "ValidatedDataType"]

DjangoModel = TypeVar("DjangoModel", bound=Union[Model, Manager])
ValidatedDataType = MutableMapping | TypedDict
