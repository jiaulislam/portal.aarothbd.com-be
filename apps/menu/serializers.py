from rest_framework.serializers import ModelSerializer, SerializerMethodField

from core.constants import AUDIT_COLUMNS

from .models import NavMenu


class MenuSerializer(ModelSerializer):
    groups = SerializerMethodField()
    child_menus = SerializerMethodField()

    class Meta:
        model = NavMenu
        exclude = AUDIT_COLUMNS

    def get_groups(self, instance: NavMenu):
        return list(instance.groups.values_list("name", flat=True))

    def get_child_menus(self, obj: NavMenu):
        child_menus = obj.child_menus.prefetch_related("child_menus").all()
        serialized = self.__class__(child_menus, many=True)
        return serialized.data
