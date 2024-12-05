from rest_framework import serializers


class BaseSerializer(serializers.Serializer):
    detail = serializers.CharField()


class SuccessResponseSerializer(BaseSerializer):
    pass
