from django.urls import path

from ..views.user_views_v1 import MeRetrieveAPIView, UserListAPIView, UserRetrieveUpdateAPIView

urlpatterns = [
    path(r"users/", UserListAPIView.as_view(), name="users-list-create"),
    path(r"users/<int:id>/", UserRetrieveUpdateAPIView.as_view(), name="users-retrieve-update"),
    path(r"me/", MeRetrieveAPIView.as_view(), name="me-retrieve"),
]
