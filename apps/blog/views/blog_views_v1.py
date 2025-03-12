from typing import TYPE_CHECKING

from django.db.models import QuerySet
from rest_framework.generics import ListCreateAPIView, RetrieveAPIView
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.permissions import AllowAny

from ..models import BlogQuerySetMixin
from ..serializers import BlogBaseSerialzer, BlogCreateSerializer, BlogDetailSerializer, BlogListSerializer
from ..services.blog_service import BlogService

if TYPE_CHECKING:
    from apps.blog.models import Blog


class BlogListCreateAPIView(ListCreateAPIView):
    permission_classes = [AllowAny]
    authentication_classes = []
    blog_service = BlogService()
    parser_classes = [MultiPartParser, FormParser]

    def get_serializer_class(self) -> type[BlogBaseSerialzer]:
        if self.request.method == "POST":
            return BlogCreateSerializer
        return BlogListSerializer

    def get_queryset(self) -> QuerySet["Blog"]:
        queryset = BlogQuerySetMixin.get_queryset()
        return queryset


class BlogRetrieveAPIView(RetrieveAPIView):
    lookup_field = "slug"
    permission_classes = [AllowAny]
    authentication_classes = []
    serializer_class = BlogDetailSerializer
    blog_service = BlogService()

    def get_queryset(self) -> QuerySet["Blog"]:
        queryset = BlogQuerySetMixin.get_queryset()
        return queryset
