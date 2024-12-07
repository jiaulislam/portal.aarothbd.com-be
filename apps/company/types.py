from core.types import BaseSerializerValidatedDataType


class CompanyValidatedDataType(BaseSerializerValidatedDataType):
    name: str
    slug: str
    bin_number: str | None
    tin_number: str | None
    addr_1: str | None
    addr_2: str | None
