from typing import TYPE_CHECKING, Any

from django.db.models import QuerySet
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from core.request import Request

from ..serializers import CommentSerializer
from ..services.comment_service import CommentService

if TYPE_CHECKING:
    from apps.blog.models import Comment


class CommentBlogCreateAPIView(GenericAPIView):
    permission_classes = [AllowAny]
    authentication_classes = []
    serializer_class = CommentSerializer
    comment_service = CommentService()

    def get_queryset(self) -> QuerySet["Comment"]:
        return self.comment_service.all()

    def post(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        serializer = self.serializer_class(data=request.data)  # type: ignore
        serializer.is_valid(raise_exception=True)
        self.comment_service.create(serializer.validated_data, request=request)
        data = {"detail": "comment posted successfully."}
        return Response(data, status=status.HTTP_201_CREATED)
