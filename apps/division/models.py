from django.db import models

from core.models import BaseModel


class Division(BaseModel):
    name = models.CharField(max_length=100)
    bn_name = models.CharField(max_length=255)
    lat = models.CharField(max_length=20, null=True, blank=True)
    long = models.FloatField(max_length=20, null=True, blank=True)

    country = models.ForeignKey("country.Country", on_delete=models.PROTECT, related_name="country_divisions")

    class Meta:
        db_table = "division_division"
        verbose_name = "division"
        verbose_name_plural = "divisions"
        ordering = ("name",)

    def __str__(self) -> str:
        return self.name
