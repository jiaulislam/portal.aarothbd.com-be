from typing import MutableMapping, TypeVar

from django.db.models import Model

__all__ = ["_T", "SerializerValidatedData"]

_T = TypeVar("_T", bound=Model)
SerializerValidatedData = MutableMapping
