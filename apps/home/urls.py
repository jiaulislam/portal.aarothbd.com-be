from django.urls import path

from .views import AdBannerListAPIView, BannerListAPIView

urlpatterns = [
    path(r"home/banners/", BannerListAPIView.as_view(), name="home-banners-list-view"),
    path(r"home/ad-banners/", AdBannerListAPIView.as_view(), name="home-ad-banners-list-view"),
]
