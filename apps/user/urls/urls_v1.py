from django.urls import path

from ..views.user_views_v1 import UserListAPIView

urlpatterns = [
    path("users/", UserListAPIView.as_view(), name="users-list-create"),
]
