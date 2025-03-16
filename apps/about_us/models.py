from django.db import models

from core.models import BaseModel
from core.storage_config import upload_banners


class AboutUs(BaseModel):
    title = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    bannger = models.ImageField(upload_to=upload_banners, null=True, blank=True)
    video_link = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        verbose_name = "About Us"
        verbose_name_plural = "About Us"

    def __str__(self):
        return self.title
