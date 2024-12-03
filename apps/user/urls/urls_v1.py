from django.urls import path

from ..views.user_views_v1 import UserListAPIView, UserRetrieveUpdateAPIView

urlpatterns = [
    path(r"users/", UserListAPIView.as_view(), name="users-list-create"),
    path(r"users/<int:id>/", UserRetrieveUpdateAPIView.as_view(), name="users-retrieve-update"),
]
