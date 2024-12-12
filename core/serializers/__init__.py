from django.db.models import TextChoices
from rest_framework import serializers


class ResponseErrorType(TextChoices):
    CLIENT_ERROR = "client_error"
    SERVER_ERROR = "server_error"


class ErrorBody(serializers.Serializer):
    code = serializers.CharField(help_text="Error code")
    detail = serializers.CharField(help_text="Error detail or message")
    attr = serializers.CharField(help_text="Error attribute field name")


class BaseSerializer(serializers.Serializer):
    detail = serializers.CharField()


class SuccessResponseSerializer(BaseSerializer):
    pass


class FailResponseSerializer(serializers.Serializer):
    type = serializers.ChoiceField(ResponseErrorType.choices)
    errors = ErrorBody(many=True)
