from typing import TYPE_CHECKING

from django.db.models import QuerySet
from rest_framework.generics import ListCreateAPIView, RetrieveAPIView
from rest_framework.permissions import AllowAny
from rest_framework.serializers import BaseSerializer

from apps.blog.constants import BlogStatusChoices

from ..serializers import BlogBaseSerialzer, BlogDetailSerializer, BlogListSerializer
from ..services.blog_service import BlogService

if TYPE_CHECKING:
    from apps.blog.models import Blog


class BlogListCreateAPIView(ListCreateAPIView):
    permission_classes = [AllowAny]
    authentication_classes = []
    blog_service = BlogService()

    def get_serializer_class(self) -> type[BaseSerializer]:
        if self.request.method == "POST":
            return BlogBaseSerialzer
        return BlogListSerializer

    def get_queryset(self) -> QuerySet["Blog"]:
        return self.blog_service.all(
            is_active=True,
            status=BlogStatusChoices.PUBLISHED,
        ).order_by("-published_on")


class BlogRetrieveAPIView(RetrieveAPIView):
    lookup_field = "slug"
    permission_classes = [AllowAny]
    authentication_classes = []
    serializer_class = BlogDetailSerializer
    blog_service = BlogService()

    def get_queryset(self) -> QuerySet["Blog"]:
        return self.blog_service.all(
            is_active=True,
            status=BlogStatusChoices.PUBLISHED,
        ).order_by("-published_on")
