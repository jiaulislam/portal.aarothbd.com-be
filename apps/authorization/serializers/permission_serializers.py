from django.contrib.auth.models import Permission
from rest_framework import serializers as s

from .content_type_serializer import ContentTypeSerializer


class PermissionSerializer(s.ModelSerializer):
    content_type = ContentTypeSerializer(read_only=True)

    class Meta:
        model = Permission
        fields = "__all__"
