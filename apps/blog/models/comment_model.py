from django.db import models

from core.models import BaseModel

__all__ = ["Comment"]


class Comment(BaseModel):
    blog = models.ForeignKey("blog.Blog", on_delete=models.CASCADE, related_name="comments")
    commented_by = models.CharField(max_length=255)
    commented_by_email = models.EmailField()
    commented_by_phone = models.CharField(max_length=20)
    commented_by_website = models.CharField(max_length=255, null=True, blank=True)
    message = models.TextField()

    def __str__(self):
        return self.commented_by

    class Meta:
        db_table = "blog_comment"
