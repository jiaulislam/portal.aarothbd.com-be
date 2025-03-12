from rest_framework import serializers as s

from core.constants.common import AUDIT_COLUMNS
from core.utils import get_serialized_data

from ..models import Blog
from .comment_serializer import CommentSerializer

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
    comments_count = s.IntegerField(read_only=True)
    created_by = s.SerializerMethodField()

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
            "list_image",
        )


class BlogDetailSerializer(s.ModelSerializer):
    created_by = s.SerializerMethodField()
    comments = CommentSerializer(read_only=True, many=True)
    comments_count = s.IntegerField(read_only=True)

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
            "body",
            "footer",
            "status",
            "is_active",
            "published_on",
            "created_by",
            "created_at",
            "comments",
            "comments_count",
            "banner",
            "list_image",
        )
