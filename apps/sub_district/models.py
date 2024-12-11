from django.db import models

from core.models import BaseModel


class SubDistrict(BaseModel):
    name = models.CharField(max_length=100)
    bn_name = models.CharField(max_length=255)
    district = models.ForeignKey("district.District", on_delete=models.CASCADE, related_name="district_sub_districts")

    class Meta:
        db_table = "sub_district_sub_district"
        verbose_name = "Sub District"
        verbose_name_plural = "Sub Districts"
        ordering = ("name",)

    def __str__(self) -> str:
        return self.name
