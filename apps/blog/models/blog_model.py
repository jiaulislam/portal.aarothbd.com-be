from typing import TYPE_CHECKING

from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils import timezone
from django.utils.text import slugify

from core.models import BaseModel

from ..constants import BlogStatusChoices

if TYPE_CHECKING:
    from apps.blog.models import Comment

__all__ = ["Blog"]


class Blog(BaseModel):
    title = models.CharField(max_length=512)
    slug = models.CharField(max_length=512, db_index=True, unique=True, null=True, blank=True)
    header = models.CharField(max_length=512, null=True, blank=True)
    body = models.TextField(null=True, blank=True)
    footer = models.TextField(max_length=512, null=True, blank=True)
    status = models.CharField(max_length=100, choices=BlogStatusChoices.choices, default=BlogStatusChoices.DRAFT)
    published_on = models.DateTimeField(null=True, blank=True)

    comments: models.QuerySet["Comment"]

    def __str__(self):
        return self.title

    class Meta:
        db_table = "blog_blog"


@receiver(pre_save, sender=Blog)
def generate_slug(sender, instance: Blog, **kwargs):
    if not instance.slug:
        instance.slug = slugify(instance.title)
        counter = 1
        original_slug = instance.slug
        while Blog.objects.filter(slug=instance.slug).exists():
            instance.slug = f"{original_slug}-{counter}"
            counter += 1

    if instance.status == BlogStatusChoices.PUBLISHED:
        instance.published_on = timezone.now()

    if instance.status == BlogStatusChoices.DRAFT and instance.published_on:
        instance.published_on = None
