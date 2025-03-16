from rest_framework.generics import ListAPIView
from rest_framework.permissions import AllowAny

from .models import Banner
from .serializers import BannerSerializer


class BannerListAPIView(ListAPIView):
    serializer_class = BannerSerializer
    queryset = Banner.objects.filter(is_active=True, ad_mode=False)
    permission_classes = [AllowAny]


class AdBannerListAPIView(ListAPIView):
    serializer_class = BannerSerializer
    queryset = Banner.objects.filter(is_active=True, ad_mode=True)
    permission_classes = [AllowAny]
