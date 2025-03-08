from django.contrib.auth import get_user_model
from django.db.models import QuerySet
from rest_framework import status
from rest_framework.generics import ListCreateAPIView, RetrieveAPIView, RetrieveUpdateAPIView, UpdateAPIView
from rest_framework.permissions import DjangoModelPermissions, IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from core.pagination import ExtendedLimitOffsetPagination

from ..filters import UserFilterSet
from ..serializers.user_serializer_v1 import (
    UserChangePasswordSerializer,
    UserDetailSerializer,
    UserSerializer,
    UserUpdateSerializer,
    UserUpdateStatusSerializer,
)
from ..services.user_service import UserService
from ..types import UserType

User = get_user_model()


class UserListCreateAPIView(ListCreateAPIView):
    serializer_class = UserSerializer
    filterset_class = UserFilterSet
    pagination_class = ExtendedLimitOffsetPagination
    permission_classes = [DjangoModelPermissions]

    user_service = UserService()

    def get_queryset(self, **kwargs) -> QuerySet[UserType]:
        queryset = self.user_service.all(is_superuser=False, select_related=["profile", "company"])
        filterset = self.filterset_class(self.request.GET, queryset=queryset)
        return filterset.qs

    def list(self, request: Request, *args, **kwargs) -> Response:
        queryset = self.get_queryset(**kwargs)
        paginate = self.pagination_class()  # type: ignore
        paginated_queryset = paginate.paginate_queryset(queryset, request)
        serialized = UserSerializer(paginated_queryset, many=True)
        return paginate.get_paginated_response(serialized.data)

    def create(self, request: Request, *args, **kwargs) -> Response:
        serialized = UserSerializer(data=request.data)
        serialized.is_valid(raise_exception=True)
        groups = serialized.validated_data.pop("groups", [])
        instance = self.user_service.create(serialized.validated_data, request=request)
        instance.groups.set(groups)
        serialized = UserSerializer(instance=instance)
        return Response(serialized.data, status=status.HTTP_201_CREATED)


class UserRetrieveUpdateAPIView(RetrieveUpdateAPIView):
    http_method_names = ["get", "put"]
    serializer_class = UserUpdateSerializer
    permission_classes = [IsAuthenticated]
    user_service = UserService()
    lookup_field = "id"

    def get_queryset(self) -> QuerySet["UserType"]:
        user: "UserType" = self.request.user  # type: ignore
        if user.is_central_admin:
            return self.user_service.all()
        return self.user_service.all(id=user.pk)

    def get_serializer_class(self):
        if self.request.method == "GET":
            return UserDetailSerializer
        return UserUpdateSerializer

    def retrieve(self, request: Request, **kwargs) -> Response:
        instance = self.get_object()
        serialized = self.get_serializer(instance)
        return Response(serialized.data, status=status.HTTP_200_OK)

    def update(self, request: Request, **kwargs) -> Response:
        serialized = UserUpdateSerializer(data=request.data)
        serialized.is_valid(raise_exception=True)
        groups = serialized.validated_data.pop("groups", [])
        instance = self.get_object()
        instance = self.user_service.update(instance, serialized.validated_data, request=request)
        instance.groups.set(groups)
        serialized = self.get_serializer(instance=instance)
        return Response(serialized.data, status=status.HTTP_200_OK)


class UserUpdateStatusAPIView(UpdateAPIView):
    http_method_names = ["patch"]
    user_service = UserService()
    serializer_class = UserUpdateStatusSerializer
    permission_classes = [DjangoModelPermissions]

    def get_queryset(self) -> QuerySet["UserType"]:
        return self.user_service.all()

    def partial_update(self, request: Request, **kwargs):
        _user_id = kwargs.get("id")
        serialized = UserUpdateStatusSerializer(data=request.data)
        serialized.is_valid(raise_exception=True)
        instance = self.user_service.get(
            id=_user_id,
            is_superuser=False,
        )
        self.user_service.update(instance, serialized.validated_data, request=request)
        return Response({"detail": "User Status updated."}, status=status.HTTP_200_OK)


class MeRetrieveAPIView(RetrieveAPIView):
    serializer_class = UserDetailSerializer
    user_service = UserService()

    def get_queryset(self) -> QuerySet["UserType"]:
        user: "UserType" = self.request.user  # type: ignore
        if user.is_central_admin:
            return self.user_service.all()
        return self.user_service.all(id=user.pk)

    def retrieve(self, request: Request, *args, **kwargs):
        current_user_id: int = request.user.id  # type: ignore
        queryset = self.user_service.get(id=current_user_id)
        user = self.user_service.get_users_permissions_groups(queryset)
        return Response(user, status=status.HTTP_200_OK)


class UserChangePasswordAPIView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserChangePasswordSerializer
    user_service = UserService()

    def post(self, request: Request, *args, **kwargs) -> Response:
        user: "UserType" = request.user  # type: ignore
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        if not user.check_password(serializer.validated_data["old_password"]):
            return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)

        self.user_service.change_password(user, serializer.validated_data["new_password"])
        # TODO: send email
        return Response({"detail": "Password changed successfully."}, status=status.HTTP_200_OK)
