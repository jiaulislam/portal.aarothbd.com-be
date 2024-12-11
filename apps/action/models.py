from django.db import models

from core.models import BaseModel


class Action(BaseModel):
    codename = models.CharField(max_length=255, unique=True)
    name = models.CharField(max_length=255, null=True, blank=True)
    property = models.JSONField(null=True, blank=True)
    help_text = models.TextField(null=True, blank=True)

    class Meta:
        db_table = "action_action"
        verbose_name_plural = "actions"
        verbose_name = "action"

    def __str__(self) -> str:
        return self.name if self.name else self.codename
