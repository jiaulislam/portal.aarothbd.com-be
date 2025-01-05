from django.contrib.auth.models import Group
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateAPIView
from rest_framework.permissions import IsAuthenticated

from ..serializers.group_serializers import GroupSerializer


class GroupListCreateAPIView(ListCreateAPIView):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [IsAuthenticated]


class GroupRetrieveUpdateAPIView(RetrieveUpdateAPIView):
    http_method_names = ["get", "put"]
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = "id"
