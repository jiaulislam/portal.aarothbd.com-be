from typing import TypedDict


class TokenResponse(TypedDict):
    refresh_token: str
    access_token: str
    iat: str
    exp: int
