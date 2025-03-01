from django.contrib import admin
from unfold.admin import TabularInline

from core.admin import BaseAdmin, InlineHelperAdmin
from core.constants.common import AUDIT_COLUMNS

from .models import Wishlist, WishlistItem


class WishlistItemInline(TabularInline, InlineHelperAdmin):
    model = WishlistItem
    extra = 0
    exclude = AUDIT_COLUMNS


@admin.register(Wishlist)
class WishlistAdmin(BaseAdmin):
    inlines = (WishlistItemInline,)
