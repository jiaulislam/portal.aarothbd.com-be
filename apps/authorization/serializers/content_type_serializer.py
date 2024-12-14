from django.contrib.contenttypes.models import ContentType
from rest_framework import serializers as s


class ContentTypeSerializer(s.ModelSerializer):
    class Meta:
        model = ContentType
        fields = "__all__"
