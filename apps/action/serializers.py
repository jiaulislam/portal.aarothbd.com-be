from rest_framework import serializers

from core.constants.serializer_constant import COMMON_EXCLUDE_FIELDS

from .models import Action


class ActionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Action
        exclude = COMMON_EXCLUDE_FIELDS + ("created_at", "updated_at")
