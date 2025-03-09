from typing import Any, Dict, Type

import jwt
from django.conf import settings
from django.db.models import Model
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError
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


def decode_jwt_token(token: str) -> dict:
    """
    Decode a JWT token.

    Args:
        token (str): The JWT token to decode.

    Returns:
        dict: The decoded payload.

    Raises:
        ExpiredSignatureError: If the token has expired.
        InvalidTokenError: If the token is invalid.
    """
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        return payload
    except ExpiredSignatureError:
        raise InvalidTokenError("Token has expired")
    except InvalidTokenError:
        raise InvalidTokenError("Invalid token")
