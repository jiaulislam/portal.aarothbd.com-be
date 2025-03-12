from rest_framework import serializers as s

from core.constants.common import AUDIT_COLUMNS
from core.utils import get_serialized_data

from ..models import Blog

__all__ = [
    "BlogBaseSerialzer",
    "BlogListSerializer",
    "BlogDetailSerializer",
    "BlogCreateSerializer",
]


class BlogBaseSerialzer(s.ModelSerializer):
    class Meta:
        model = Blog
        exclude = AUDIT_COLUMNS


class BlogCreateSerializer(BlogBaseSerialzer):
    class Meta:
        model = Blog
        exclude = AUDIT_COLUMNS + ("slug", "published_on")


class BlogListSerializer(BlogBaseSerialzer):
    comments_count = s.SerializerMethodField()
    created_by = s.SerializerMethodField()

    def get_comments_count(self, obj: Blog):
        comments_count = obj.comments.filter(created_by__isnull=True).count()
        return comments_count

    def get_created_by(self, obj: Blog):
        from apps.user.serializers.user_serializer_v1 import UserSerializer

        data = get_serialized_data(UserSerializer, obj, "created_by")
        return data

    class Meta:
        model = Blog
        fields = (
            "id",
            "slug",
            "title",
            "header",
            "created_by",
            "published_on",
            "comments_count",
        )


class BlogDetailSerializer(s.ModelSerializer):
    created_by = s.SerializerMethodField()
    comments = s.SerializerMethodField()
    comments_count = s.SerializerMethodField()

    def get_created_by(self, obj: Blog):
        from apps.user.serializers.user_serializer_v1 import UserSerializer

        data = get_serialized_data(UserSerializer, obj, "created_by")
        return data

    def get_comments(self, obj: Blog):
        from apps.blog.serializers import CommentSerializer

        data = get_serialized_data(CommentSerializer, obj, "comments", many=True)
        return data

    def get_comments_count(self, obj: Blog):
        comments_count = obj.comments.filter(created_by__isnull=True).count()
        return comments_count

    class Meta:
        model = Blog
        fields = (
            "id",
            "slug",
            "title",
            "header",
            "body",
            "footer",
            "status",
            "is_active",
            "published_on",
            "created_by",
            "created_at",
            "comments",
            "comments_count",
        )
