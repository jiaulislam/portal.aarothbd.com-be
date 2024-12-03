from typing import Any, MutableMapping, TypeVar, Union

from django.db.models import Model

__all__ = ["_T", "SerializerValidatedData"]

_T = TypeVar("_T", bound=Model)

SerializerValidatedData = MutableMapping[str, Union[str, int, Any]]
