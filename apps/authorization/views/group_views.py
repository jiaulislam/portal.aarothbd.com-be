from django.contrib.auth.models import Group
from rest_framework.generics import ListCreateAPIView
from rest_framework.permissions import IsAuthenticated

from ..serializers.group_serializers import GroupSerializer


class GroupListCreateAPIView(ListCreateAPIView):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [IsAuthenticated]
