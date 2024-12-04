from django.db import models

from core.models.base_model import BaseModel


class Address(BaseModel):
    line_1 = models.TextField(null=True, blank=True)
    line_2 = models.TextField(null=True, blank=True)

    class Meta:
        db_table = "address_address"

    def __str__(self) -> str:
        return f"{str(self.pk)} / {self.line_1} / {self.line_2}"
