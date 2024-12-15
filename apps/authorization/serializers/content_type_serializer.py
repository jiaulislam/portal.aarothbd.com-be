from django.apps import apps
from django.contrib.contenttypes.models import ContentType
from rest_framework import serializers as s

from .permission_serializers import PermissionSerializer


class ContentTypeSerializer(s.ModelSerializer):
    permissions = PermissionSerializer(read_only=True, many=True, source="permission_set")
    model_name = s.SerializerMethodField()

    def get_model_name(self, object: ContentType):
        model_class = apps.get_model(object.app_label, object.model)
        model_name = "".join(" " + name if name.isupper() else name for name in model_class.__name__)
        return model_name.strip()

    class Meta:
        model = ContentType
        fields = ("id", "app_label", "model", "model_name", "permissions")
