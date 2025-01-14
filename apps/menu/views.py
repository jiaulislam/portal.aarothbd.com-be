from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_headers
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from core.authentication import SecureCookieAuthentication
from core.request import Request

from .models import NavMenu
from .serializers import MenuSerializer
from .services import NavMenuService

CACHING_TIME = 60 * 60 * 2  # 2 Hour


class MenuViewSet(ViewSet):
    serializer_class = MenuSerializer
    authentication_classes = [SecureCookieAuthentication]
    pagination_class = None
    permission_classes = [IsAuthenticated]

    nav_menu_service = NavMenuService()

    def get_queryset(self):
        user = self.request.user
        return self.nav_menu_service.get_root_menus(user)

    @method_decorator(cache_page(CACHING_TIME))
    @method_decorator(vary_on_headers("accessToken"))
    def list(self, request: Request, *args, **kwargs):
        queryset = self.get_queryset()
        serialized = self.serializer_class(queryset, many=True)
        return Response(serialized.data)

    class Meta:
        model = NavMenu
