from django.urls import path

from .views import WishlistItemListCreateAPIView, WishlistItemRemoveAPIView

urlpatterns = [
    path("wishlist/items/remove/", WishlistItemRemoveAPIView.as_view(), name="wishlist-item-remove-view"),
    path("wishlist/items/", WishlistItemListCreateAPIView.as_view(), name="wishlist-item-add-view"),
]
