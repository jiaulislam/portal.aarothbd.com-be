from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from core.authentication import SecureCookieAuthentication
from core.request import Request

from .models import NavMenu
from .serializers import MenuSerializer
from .services import NavMenuService


class MenuViewSet(ViewSet):
    serializer_class = MenuSerializer
    authentication_classes = [SecureCookieAuthentication]
    pagination_class = None
    permission_classes = [IsAuthenticated]

    nav_menu_service = NavMenuService()

    def get_queryset(self):
        user = self.request.user
        return self.nav_menu_service.get_root_menus(user)

    def list(self, request: Request, *args, **kwargs):
        queryset = self.get_queryset()
        serialized = self.serializer_class(queryset, many=True)
        return Response(serialized.data)

    class Meta:
        model = NavMenu
