from django.contrib.auth.models import Permission
from rest_framework import serializers as s


class PermissionSerializer(s.ModelSerializer):
    class Meta:
        model = Permission
        fields = ("id", "name", "codename")
