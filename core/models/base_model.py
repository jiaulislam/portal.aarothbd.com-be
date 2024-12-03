from django.db import models


class BaseModel(models.Model):
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        "user.User",
        related_name="%(app_label)s_%(class)s_created",
        on_delete=models.DO_NOTHING,
        null=True,
        blank=True,
    )
    updated_by = models.ForeignKey(
        "user.User",
        related_name="%(app_label)s_%(class)s_updated",
        on_delete=models.DO_NOTHING,
        null=True,
        blank=True,
    )

    class Meta:
        abstract = True
