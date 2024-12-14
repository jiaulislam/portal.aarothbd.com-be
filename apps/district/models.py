from django.db import models

from core.models import BaseModel


class District(BaseModel):
    name = models.CharField(max_length=100)
    bn_name = models.CharField(max_length=255)
    lat = models.CharField(max_length=20, null=True, blank=True)
    long = models.CharField(max_length=20, null=True, blank=True)
    division = models.ForeignKey("division.Division", on_delete=models.PROTECT)

    class Meta:
        db_table = "district_district"
        verbose_name = "district"
        verbose_name_plural = "districts"
        ordering = ("name",)

    def __str__(self) -> str:
        return self.name
