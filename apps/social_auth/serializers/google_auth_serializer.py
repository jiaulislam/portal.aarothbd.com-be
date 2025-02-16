from rest_framework import serializers as s

__all__ = ["GoogleAuthLoginSerializer"]


class GoogleAuthLoginSerializer(s.Serializer):
    id_token = s.CharField()
