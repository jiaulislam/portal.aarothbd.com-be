from rest_framework import serializers

from .models import PolicyModel


class PolicyModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = PolicyModel
        fields = ["id", "title", "subtitle", "description"]
