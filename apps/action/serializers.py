from rest_framework import serializers

from core.constants import COMMON_EXCLUDE_FIELDS

from .models import Action


class ActionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Action
        exclude = COMMON_EXCLUDE_FIELDS + ("created_at", "updated_at")


class ActionExecuteSerializer(serializers.Serializer):
    action_name = serializers.CharField(required=True, allow_null=False, allow_blank=False)
