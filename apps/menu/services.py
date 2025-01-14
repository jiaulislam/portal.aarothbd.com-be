from apps.user.models import User
from core.services import BaseModelService

from .models import NavMenu


class NavMenuService(BaseModelService):
    model_class = NavMenu

    def get_root_menus(self, user: User):
        groups = user.groups.all()
        root_menus = set()
        for group in groups:
            root_menus = root_menus.union(group.nav_menus.filter(parent_menu__isnull=True))

        return root_menus
