from django.contrib.auth import get_user_model
from django.db.models import QuerySet
from rest_framework import status
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.generics import GenericAPIView
from rest_framework.request import Request
from rest_framework.response import Response

from core.pagination import ExtendedLimitOffsetPagination

from ..filters import UserFilterSet
from ..serializers.user_serializer_v1 import (
    UserSerializer,
    UserUpdateStatusSerializer,
)
from ..services.user_service import UserService
from ..types import UserType

User = get_user_model()


class UserListCreateAPIView(GenericAPIView):
    serializer_class = UserSerializer
    filterset_class = UserFilterSet
    pagination_class = ExtendedLimitOffsetPagination

    user_service = UserService()

    def get_queryset(self, **kwargs) -> QuerySet[UserType]:
        queryset = self.user_service.all(is_superuser=False, **kwargs)
        filterset = self.filterset_class(self.request.GET, queryset=queryset)
        return filterset.qs

    def get(self, request: Request, *args, **kwargs) -> Response:
        queryset = self.get_queryset(**kwargs)
        paginate = self.pagination_class()  # type: ignore
        paginated_queryset = paginate.paginate_queryset(queryset, request)
        serialized = self.serializer_class(paginated_queryset, many=True)  # type: ignore
        return paginate.get_paginated_response(serialized.data)

    def post(self, request: Request, *args, **kwargs) -> Response:
        serialized = self.serializer_class(data=request.data)  # type: ignore
        serialized.is_valid(raise_exception=True)
        instance = self.user_service.create(serialized.data)
        serialized = self.serializer_class(instance=instance)  # type: ignore
        return Response(serialized.data, status=status.HTTP_201_CREATED)


class UserRetrieveUpdateAPIView(GenericAPIView):
    serializer_class = UserSerializer
    user_service = UserService()

    def get_queryset(self, id: int) -> UserType | None:
        return self.user_service.get(
            id=id,
            is_superuser=False,
            select_related=["profile"],
            prefetch_related=["groups", "user_permissions"],
        )

    def get(self, request: Request, id: int, **kwargs) -> Response:
        queryset = self.get_queryset(id)
        serialized = self.serializer_class(queryset)  # type: ignore
        return Response(serialized.data, status=status.HTTP_200_OK)


class UserUpdateStatusAPIView(GenericAPIView):
    user_service = UserService()
    serializer_class = UserUpdateStatusSerializer

    def get_queryset(self, id: int) -> UserType:
        return self.user_service.get(
            id=id,
            is_superuser=False,
            select_related=["profile"],
            prefetch_related=["groups", "user_permissions"],
        )

    def post(self, request: Request, id: int, **kwargs):
        serialized = self.serializer_class(data=request.data)  # type: ignore
        serialized.is_valid(raise_exception=True)
        instance = self.get_queryset(id)
        self.user_service.update(instance, serialized.data, request=request)
        return Response({"detail": "User Status updated."}, status=status.HTTP_200_OK)


class MeRetrieveAPIView(GenericAPIView):
    serializer_class = UserSerializer
    use_service = UserService()

    def get_queryset(self, current_user_id: int) -> UserType:
        return self.use_service.get(id=current_user_id)

    def get(self, request: Request, *args, **kwargs):
        current_user_id: int | None = request.user.id
        if not current_user_id:
            raise AuthenticationFailed()
        queryset = self.get_queryset(current_user_id)
        serialized = self.serializer_class(queryset)  # type: ignore
        return Response(serialized.data, status=status.HTTP_200_OK)
