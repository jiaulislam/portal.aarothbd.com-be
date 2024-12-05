from typing import NotRequired, TypedDict

from core.types.model_type import BaseSerializerValidatedDataType


class TokenResponse(TypedDict, total=False):
    refresh_token: str
    access_token: str
    iat: str
    exp: int


class RegisterUserValidatedDataType(BaseSerializerValidatedDataType):
    email: str
    first_name: NotRequired[str]
    last_name: NotRequired[str]
    password: str
    password2: NotRequired[str]
