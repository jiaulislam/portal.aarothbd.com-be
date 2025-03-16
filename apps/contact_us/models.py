from django.contrib.postgres.fields import ArrayField
from django.db import models

from core.models import BaseModel


class ContactUs(BaseModel):
    name = models.CharField(max_length=255)
    email = models.EmailField(null=True, blank=True)
    phone = models.CharField(max_length=20, null=True, blank=True)
    subject = models.CharField(max_length=255)
    message = models.TextField()
    is_mail_sent = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Contact Us"
        verbose_name_plural = "Contact Us"

    def __str__(self):
        return self.name


class EmailRecepient(BaseModel):
    to_email = models.EmailField()
    cc_email = ArrayField(models.EmailField(), null=True, blank=True)
    bcc_email = ArrayField(models.EmailField(), null=True, blank=True)

    class Meta:
        verbose_name = "Email Recepient"
        verbose_name_plural = "Email Recepients"

    def __str__(self):
        return self.to_email
