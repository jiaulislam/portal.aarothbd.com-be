from typing import Final, Tuple

COMMON_EXCLUDE_FIELDS: Final[Tuple[str, str]] = (
    "created_by",
    "updated_by",
)


STATUS_SERIALIZER_FIELDS: Final[Tuple[str, str]] = (
    "id",
    "is_active",
)
