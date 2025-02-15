from typing import TYPE_CHECKING, Any

from django.db.models import QuerySet
from rest_framework.generics import ListCreateAPIView, RetrieveAPIView
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response
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

    def list(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        queryset = self.get_queryset()
        serializer = self.get_serializer_class()(queryset, many=True)
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
