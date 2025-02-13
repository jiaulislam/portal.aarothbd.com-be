from typing import Any, Dict, Type

from django.db.models import Model
from rest_framework.serializers import BaseSerializer

T = Type[BaseSerializer]


def get_serialized_data(serializer_class: T, instance: Model, key: str, many: bool = False) -> Dict[str, Any]:
    """
    Retrieves serialized data for a related object using the specified serializer class.

    Args:
        serializer_class (Type[BaseSerializer]): The serializer class to use for serialization.
        instance (Model): The object containing the related data.
        key (str): The attribute name on `instance` that holds the related data.
        many (bool, optional): Whether the related data is a collection (defaults to False).

    Returns:
        Any: Serialized data from the specified serializer.

    Raises:
        AttributeError: If the specified `key` does not exist on `instance`.

    Example:
        >>> get_related_serializer_data(MySerializer, my_object, "related_field", many=True)
    """
    object_key = getattr(instance, key)
    serializer = serializer_class(object_key, many=many)
    return serializer.data
