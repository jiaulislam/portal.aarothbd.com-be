from django.db import models

from core.models import BaseModel


class Country(BaseModel):
    name = models.CharField(max_length=255)
    full_name = models.CharField(verbose_name="Full Name", max_length=255, null=True, blank=True)
    country_code = models.CharField(verbose_name="Country Code", max_length=2, unique=True)
    country_code_alpha3 = models.CharField(verbose_name="Country Code (Alpha-3)", max_length=3, unique=True)
    country_code_iso3 = models.CharField(verbose_name="Country Code (ISO-3)", max_length=3, unique=True)
    continent_code = models.CharField(verbose_name="Continent Code", max_length=2)
    continent_name = models.CharField(verbose_name="Continent Name", max_length=255, null=True, blank=True)


    class Meta:
        db_table = 'country_country'
        verbose_name = 'Country'
        verbose_name_plural = 'Countries'
        ordering = ('name',)

    def __str__(self) -> str:
        return self.name
