from django.db import models

from core.models import BaseModel

from .constants import SMSStatusChoice


class SMSLog(BaseModel):
    phone = models.CharField(max_length=20)
    message = models.TextField(null=False, blank=False)
    status = models.CharField(max_length=20, choices=SMSStatusChoice.choices, default=SMSStatusChoice.PENDING)
    response = models.JSONField(null=True, blank=True)

    class Meta:
        db_table = "sms_service_sms_log"
        verbose_name = "SMS Log"
        verbose_name_plural = "SMS Logs"
