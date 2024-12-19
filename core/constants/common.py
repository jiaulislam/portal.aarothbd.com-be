from typing import Final

COMMON_EXCLUDE_FIELDS: Final = (
    "created_by",
    "updated_by",
)


STATUS_SERIALIZER_FIELDS: Final = (
    "id",
    "is_active",
)


AUDIT_COLUMNS: Final = ("created_at", "updated_at", "created_by", "updated_by")
