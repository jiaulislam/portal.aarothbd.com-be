from django.contrib.auth.models import Permission
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated

from ..serializers.permission_serializers import PermissionSerializer


class PermissionListAPIView(ListAPIView):
    queryset = Permission.objects.all()
    serializer_class = PermissionSerializer
    permission_classes = [IsAuthenticated]
