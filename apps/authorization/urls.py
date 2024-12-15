from django.urls import path

from .views.content_type_views import ContentTypeListAPIView, ContentTypePermissionListAPIView
from .views.group_views import GroupListCreateAPIView
from .views.permission_views import PermissionListAPIView

urlpatterns = [
    path(r"auth/content-types/", ContentTypeListAPIView.as_view(), name="content-types-list"),
    path(
        r"auth/content-types/<int:contenttype_id>/permissions/",
        ContentTypePermissionListAPIView.as_view(),
        name="content-types-list",
    ),
    path(r"auth/permissions/", PermissionListAPIView.as_view(), name="permissions-list"),
    path(r"auth/groups/", GroupListCreateAPIView.as_view(), name="group-create-view"),
]
