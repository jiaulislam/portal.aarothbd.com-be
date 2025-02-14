from typing import TYPE_CHECKING, Any

from django.db.models import QuerySet
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response

from apps.blog.constants import BlogStatusChoices

from ..serializers import BlogDetailSerializer, BlogListSerializer
from ..services.blog_service import BlogService

if TYPE_CHECKING:
    from apps.blog.models import Blog


class BlogListAPIView(ListAPIView):
    permission_classes = [AllowAny]
    authentication_classes = []
    serializer_class = BlogListSerializer
    blog_service = BlogService()

    def get_queryset(self) -> QuerySet["Blog"]:
        return self.blog_service.all(
            is_active=True,
            status=BlogStatusChoices.PUBLISHED,
        ).order_by("-published_on")

    def list(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        queryset = self.get_queryset()
        serializer = self.serializer_class(queryset, many=True)  # type: ignore
        return Response(serializer.data)


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

    def retrieve(self, request: Request, slug: str, *args: Any, **kwargs: Any) -> Response:
        queryset = self.get_queryset().get(slug=slug)
        serializer = self.serializer_class(queryset)  # type: ignore
        return Response(serializer.data)
