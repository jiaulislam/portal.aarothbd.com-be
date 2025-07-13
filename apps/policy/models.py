from django.db import models

from core.models import BaseModel


class PolicyModel(BaseModel):
    title = models.CharField(max_length=255)
    subtitle = models.CharField(max_length=255, null=True, blank=True)
    description = models.TextField(null=True)
    order = models.IntegerField(default=0)  # new field

    def __str__(self):
        return self.title

    class Meta:
        db_table = "policy_policy"
        verbose_name = "Policy"
        verbose_name_plural = "Policies"
