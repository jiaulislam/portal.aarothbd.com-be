from django.contrib.auth.models import Group
from rest_framework import serializers as s


class GroupSerializer(s.ModelSerializer):
    permissions_count = s.SerializerMethodField()
    users_count = s.SerializerMethodField()

    def get_permissions_count(self, object: Group) -> int:
        return object.permissions.count()

    def get_users_count(self, object: Group) -> int:
        return object.user_set.count()

    class Meta:
        model = Group
        fields = ["id", "name", "permissions_count", "users_count", "permissions"]
