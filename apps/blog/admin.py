from django.contrib import admin
from unfold.admin import TabularInline

from core.admin import BaseAdmin, InlineHelperAdmin
from core.constants.common import AUDIT_COLUMNS

from .models import Blog, Comment


class CommentInlines(TabularInline, InlineHelperAdmin):
    model = Comment
    extra = 0
    exclude = AUDIT_COLUMNS
    show_change_link = False
    verbose_name = "Comment"
    verbose_name_plural = "Comments"


@admin.register(Blog)
class BlogAdmin(BaseAdmin):
    list_display = (
        "slug",
        "title",
        "published_on",
        "created_by",
        "status",
        "is_active",
    )
    list_filter = ("status",)
    search_fields = ("title", "header", "footer", "slug")

    inlines = (CommentInlines,)
    readonly_fields = ("created_at", "updated_at", "updated_by")

    save_as = True
