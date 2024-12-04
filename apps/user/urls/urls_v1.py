from django.urls import path

from ..views import MeRetrieveAPIView, UserListCreateAPIView, UserRetrieveUpdateAPIView

urlpatterns = [
    path(r"users/", UserListCreateAPIView.as_view(), name="users-list-create"),
    path(r"users/<int:id>/", UserRetrieveUpdateAPIView.as_view(), name="users-retrieve-update"),
    path(r"me/", MeRetrieveAPIView.as_view(), name="me-retrieve"),
]
