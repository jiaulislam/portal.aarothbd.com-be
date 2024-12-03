from typing import MutableMapping, TypeVar, Union

from django.db.models import Manager, Model, QuerySet

__all__ = ["DjangoModel", "ValidatedDataType"]

DjangoModel = TypeVar("DjangoModel", bound=Union[Model, Manager, QuerySet])
ValidatedDataType = MutableMapping
