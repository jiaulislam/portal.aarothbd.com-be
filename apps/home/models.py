from django.db import models

from core.models import BaseModel
from core.storage_config import upload_banners


class Banner(BaseModel):
    title = models.CharField(max_length=255)
    image = models.ImageField(upload_to=upload_banners)
    alt_text = models.CharField(max_length=255)
    link = models.URLField()
    order = models.IntegerField(default=0)
    ad_mode = models.BooleanField(default=False)

    class Meta:
        db_table = "home_banner"
        ordering = ["order"]

    def __str__(self):
        return self.title
