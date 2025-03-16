from django.db import models

from core.models import BaseModel
from core.storage_config.file_path import upload_general_image


class Testimonial(BaseModel):
    client_name = models.CharField(max_length=255)
    client_position = models.CharField(max_length=255)
    client_image = models.ImageField(upload_to=upload_general_image)
    client_comment = models.TextField()

    def __str__(self):
        return self.client_name

    class Meta:
        verbose_name = "Testimonial"
        verbose_name_plural = "Testimonials"
        ordering = ["-created_at"]
