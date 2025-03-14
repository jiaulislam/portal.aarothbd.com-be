from django.db import models

from core.services import BaseModelService

from ..constants import BlogStatusChoices
from ..models import Blog


class BlogService(BaseModelService[Blog]):
    model_class = Blog

    def get_published_queryset(self) -> models.QuerySet["Blog"]:
        queryset = (
            self.model_class.objects.filter(
                is_active=True,
                status=BlogStatusChoices.PUBLISHED,
            )
            .annotate(
                comments_count=models.Count(
                    "comments",
                    filter=models.Q(
                        comments__created_by__isnull=True,
                        comments__is_active=True,
                    ),
                )
            )
            .select_related("created_by", "created_by__profile", "created_by__company")
            .prefetch_related("created_by__groups")
            .order_by("-published_on")
        )
        return queryset
