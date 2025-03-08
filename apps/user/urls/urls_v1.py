from django.urls import path

from ..views import (
    MeRetrieveAPIView,
    UserChangePasswordAPIView,
    UserListCreateAPIView,
    UserRetrieveUpdateAPIView,
    UserUpdateStatusAPIView,
)

urlpatterns = [
    path(r"users/", UserListCreateAPIView.as_view(), name="users-list-create"),
    path(r"users/<int:id>/", UserRetrieveUpdateAPIView.as_view(), name="user-retrieve-update"),
    path(r"users/<int:id>/update-status/", UserUpdateStatusAPIView.as_view(), name="user-update-status"),
    path(r"users/<int:id>/change-password/", UserChangePasswordAPIView.as_view(), name="user-change-password"),
    path(r"me/", MeRetrieveAPIView.as_view(), name="me-retrieve"),
]
