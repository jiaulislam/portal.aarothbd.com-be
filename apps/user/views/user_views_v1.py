from django.contrib.auth import get_user_model
from django.db.models import QuerySet
from rest_framework import status
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

    def get(self, _: Request, *args, **kwargs):
        queryset = self.get_queryset(**kwargs)
        serialized = self.serializer_class(queryset, many=True)  # type: ignore
        return Response(serialized.data, status=status.HTTP_200_OK)
