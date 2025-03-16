from debug_toolbar.toolbar import debug_toolbar_urls
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)

api_v1 = "api/v1/"
api_v2 = "api/v2/"

urlpatterns = [
    path("admin/", admin.site.urls),
]

admin.site.site_header = "aarothbd.com"
admin.site.index_title = "Aaroth BD Administration"

v1_routes = [
    path(api_v1, include("apps.authentication.urls.urls_v1")),
    path(api_v1, include("apps.authorization.urls")),
    path(api_v1, include("apps.user.urls.urls_v1")),
    path(api_v1, include("apps.menu.urls")),
    path(api_v1, include("apps.company.urls.urls_v1")),
    path(api_v1, include("apps.action.urls")),
    path(api_v1, include("apps.country.urls")),
    path(api_v1, include("apps.district.urls")),
    path(api_v1, include("apps.division.urls")),
    path(api_v1, include("apps.sub_district.urls")),
    path(api_v1, include("apps.address.urls")),
    path(api_v1, include("apps.uom.urls")),
    path(api_v1, include("apps.product.urls.product_urls_v1")),
    path(api_v1, include("apps.sale_order.urls.urls_v1")),
    path(api_v1, include("apps.blog.urls")),
    path(api_v1, include("apps.social_auth.urls")),
    path(api_v1, include("apps.offer.urls")),
    path(api_v1, include("apps.wishlist.urls")),
    path(api_v1, include("apps.customer_order.urls")),
    path(api_v1, include("apps.about_us.urls")),
    path(api_v1, include("apps.business_partner.urls")),
    path(api_v1, include("apps.contact_us.urls")),
    path(api_v1, include("apps.home.urls")),
    path(api_v1, include("apps.testimonial.urls")),
    path(
        f"{api_v1}schema/",
        SpectacularAPIView.as_view(api_version="v1"),
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


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
