from django.contrib.auth.models import Group
from rest_framework import serializers as s


class GroupSerializer(s.ModelSerializer):
    class Meta:
        model = Group
        fields = '__all__'
