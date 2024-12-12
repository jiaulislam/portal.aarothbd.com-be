from django.contrib.auth import get_user_model
from django.db.models import QuerySet
from rest_framework import status
from rest_framework.generics import ListCreateAPIView, RetrieveAPIView, RetrieveUpdateAPIView, UpdateAPIView
from rest_framework.request import Request
from rest_framework.response import Response

from core.pagination import ExtendedLimitOffsetPagination

from ..filters import UserFilterSet
from ..serializers.user_serializer_v1 import (
    UserDetailSerializer,
    UserSerializer,
    UserUpdateStatusSerializer,
)
from ..services.user_service import UserService
from ..types import UserType

User = get_user_model()


class UserListCreateAPIView(ListCreateAPIView):
    serializer_class = UserSerializer
    filterset_class = UserFilterSet
    pagination_class = ExtendedLimitOffsetPagination

    user_service = UserService()

    def get_queryset(self, **kwargs) -> QuerySet[UserType]:
        queryset = self.user_service.all(is_superuser=False, select_related=["profile", "company"])
        filterset = self.filterset_class(self.request.GET, queryset=queryset)
        return filterset.qs

    def list(self, request: Request, *args, **kwargs) -> Response:
        queryset = self.get_queryset(**kwargs)
        paginate = self.pagination_class()  # type: ignore
        paginated_queryset = paginate.paginate_queryset(queryset, request)
        serialized = self.serializer_class(paginated_queryset, many=True)  # type: ignore
        return paginate.get_paginated_response(serialized.data)

    def create(self, request: Request, *args, **kwargs) -> Response:
        serialized = self.serializer_class(data=request.data)  # type: ignore
        serialized.is_valid(raise_exception=True)
        instance = self.user_service.create(serialized.validated_data, request=request)
        serialized = self.serializer_class(instance=instance)  # type: ignore
        return Response(serialized.data, status=status.HTTP_201_CREATED)


class UserRetrieveUpdateAPIView(RetrieveUpdateAPIView):
    http_method_names = ["get", "put"]
    serializer_class = UserSerializer
    detail_serializer_class = UserDetailSerializer
    user_service = UserService()

    def retrieve(self, request: Request, **kwargs) -> Response:
        _user_id = kwargs.get("id")
        queryset = self.user_service.get(
            id=_user_id,
            is_superuser=False,
            select_related=["profile"],
            prefetch_related=["groups", "user_permissions"],
        )
        serialized = self.detail_serializer_class(queryset)  # type: ignore
        return Response(serialized.data, status=status.HTTP_200_OK)

    def update(self, request: Request, **kwargs) -> Response:
        _user_id = kwargs.get("id")
        serialized = self.serializer_class(data=request.data)
        serialized.is_valid(raise_exception=True)
        serialized.validated_data.pop("email", None)  # never update user email
        instance = self.user_service.get(id=_user_id, is_superuser=False)
        instance = self.user_service.update(instance, serialized.validated_data, request=request)
        serialized = self.serializer_class(instance=instance)
        return Response(serialized.data, status=status.HTTP_200_OK)


class UserUpdateStatusAPIView(UpdateAPIView):
    http_method_names = ["patch"]
    user_service = UserService()
    serializer_class = UserUpdateStatusSerializer

    def partial_update(self, request: Request, **kwargs):
        _user_id = kwargs.get("id")
        serialized = self.serializer_class(data=request.data)  # type: ignore
        serialized.is_valid(raise_exception=True)
        instance = self.user_service.get(
            id=_user_id,
            is_superuser=False,
            select_related=["profile"],
            prefetch_related=["groups", "user_permissions"],
        )
        self.user_service.update(instance, serialized.validated_data, request=request)
        return Response({"detail": "User Status updated."}, status=status.HTTP_200_OK)


class MeRetrieveAPIView(RetrieveAPIView):
    serializer_class = UserDetailSerializer
    user_service = UserService()

    def retrieve(self, request: Request, *args, **kwargs):
        current_user_id: int = request.user.id
        queryset = self.user_service.get(id=current_user_id)
        serialized = self.serializer_class(queryset)  # type: ignore
        return Response(serialized.data, status=status.HTTP_200_OK)
