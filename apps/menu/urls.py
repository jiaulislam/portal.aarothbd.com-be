from django.urls import path

from .views import MenuViewSet

urlpatterns = [
    path("menus/", MenuViewSet.as_view({"get": "list"}), name="menus"),
]
