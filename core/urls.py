from debug_toolbar.toolbar import debug_toolbar_urls
from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)
from rest_framework.settings import api_settings

api_v1 = "api/v1/"
api_v2 = "api/v2/"

urlpatterns = [
    path("admin/", admin.site.urls),
]

v1_routes = [
    path(api_v1, include(("apps.user.urls.urls_v1", "users"), namespace="users-v1")),
    path(api_v1, include(("apps.authentication.urls.urls_v1", "auths"), namespace="auth-v1")),
    path(
        f"{api_v1}schema/",
        SpectacularAPIView.as_view(api_version="v1", renderer_classes=api_settings.DEFAULT_RENDERER_CLASSES),
        name="schema-v1",
    ),
    path(
        f"{api_v1}docs/",
        SpectacularSwaggerView.as_view(url_name="schema-v1"),
        name="swagger-ui",
    ),
    path(
        f"{api_v1}redoc/",
        SpectacularRedocView.as_view(url_name="schema-v1"),
        name="redoc",
    ),
]


versioned_routes = [v1_routes]

for routes in versioned_routes:
    urlpatterns.extend(routes)


urlpatterns += debug_toolbar_urls()
