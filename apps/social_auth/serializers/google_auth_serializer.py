from rest_framework import serializers as s

__all__ = ["GoogleAuthLoginSerializer"]


class GoogleAuthLoginSerializer(s.Serializer):
    auth_code = s.CharField()
