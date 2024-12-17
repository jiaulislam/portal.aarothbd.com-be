from rest_framework.permissions import SAFE_METHODS, BasePermission, IsAdminUser
from rest_framework.views import APIView

from apps.user.constants import UserTypeChoices
from core.request import Request

__all__ = ["IsSuperAdmin", "IsCentralAdminOrReadOnly"]


class IsSuperAdmin(IsAdminUser):
    def has_permission(self, request: Request, view: APIView) -> bool:
        return bool(request.user and (request.user.is_superuser or request.user.is_staff))


class IsCentralAdminOrReadOnly(BasePermission):
    def has_permission(self, request: Request, view: APIView) -> bool:
        if view.request.method in SAFE_METHODS:
            return True

        return bool(
            request.user
            and (
                request.user.is_staff
                or request.user.is_superuser
                or request.user.user_type == UserTypeChoices.CENTRAL_ADMIN  # type: ignore
            )
        )
