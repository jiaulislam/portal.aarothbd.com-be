from rest_framework import viewsets

from .models import PolicyModel
from .serializers import PolicyModelSerializer


class PolicyModelViewSet(viewsets.ModelViewSet):
    queryset = PolicyModel.objects.filter(is_active=True).order_by("order")  # order by ascending
    serializer_class = PolicyModelSerializer
