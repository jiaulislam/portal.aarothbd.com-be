from django.contrib.auth import get_user_model
from django.db.models import QuerySet
from rest_framework import status
from rest_framework.exceptions import NotFound
from rest_framework.generics import GenericAPIView
from rest_framework.request import Request
from rest_framework.response import Response

from ..filters import UserFilterSet
from ..serializers.user_serializer_v1 import (
    UserSerializer,
)
from ..services.user_service import UserService
from ..types import UserType

User = get_user_model()


class UserListAPIView(GenericAPIView):
    authentication_classes = []
    permission_classes = []
    serializer_class = UserSerializer
    filterset_class = UserFilterSet

    user_service = UserService()

    def get_queryset(self, **kwargs) -> QuerySet[UserType]:
        queryset = self.user_service.all(is_superuser=False, **kwargs)
        filterset = self.filterset_class(self.request.GET, queryset=queryset)
        return filterset.qs

    def get(self, _: Request, *args, **kwargs) -> Response:
        queryset = self.get_queryset(**kwargs)
        serialized = self.serializer_class(queryset, many=True)  # type: ignore
        return Response(serialized.data, status=status.HTTP_200_OK)

    def handle_exception(self, exc: Exception) -> Response:
        return super().handle_exception(exc)


class UserRetrieveUpdateAPIView(GenericAPIView):
    authentication_classes = []
    permission_classes = []
    serializer_class = UserSerializer
    user_service = UserService()

    def get_queryset(self, id: int) -> UserType | None:
        return self.user_service.all(id=id, is_superuser=False).first()

    def get(self, request: Request, id: int, **kwargs) -> Response:
        queryset = self.get_queryset(id)
        if not queryset:
            raise NotFound(detail="No User matches the given query.")
        serialized = self.serializer_class(queryset)  # type: ignore
        return Response(serialized.data, status=status.HTTP_200_OK)

    def handle_exception(self, exc: Exception) -> Response:
        return super().handle_exception(exc)
