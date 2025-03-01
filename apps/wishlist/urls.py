from django.urls import path

from .views import WishlistItemListAddAPIView, WishlistItemRemoveAPIView

urlpatterns = [
    path("wishlist/items/remove/", WishlistItemRemoveAPIView.as_view(), name="wishlist-item-remove-view"),
    path("wishlist/items/", WishlistItemListAddAPIView.as_view(), name="wishlist-item-add-view"),
]
