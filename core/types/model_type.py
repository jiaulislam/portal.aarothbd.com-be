from typing import MutableMapping, TypeVar

from django.db.models import Model

__all__ = ["_T", "SerializedValidatedData"]

_T = TypeVar("_T", bound=Model)
SerializedValidatedData = MutableMapping
