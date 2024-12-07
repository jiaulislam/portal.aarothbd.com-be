from django.db import models

from core.models import BaseModel

from .company_model import Company

__all__ = ["CompanyConfiguration"]


class CompanyConfiguration(BaseModel):
    company = models.OneToOneField(Company, on_delete=models.CASCADE, related_name="configuration")
    can_change_theme_color = models.BooleanField(default=False)
    can_see_beta_features = models.BooleanField(default=False)

    class Meta:
        db_table = "company_company_configuration"

    def __str__(self) -> str:
        return f"{self.pk} - {self.company.name}"
