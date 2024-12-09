from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from .filters import ActionFilter
from .serializers import ActionSerializer
from .services import ActionService


class ActionListAPIView(GenericAPIView):
    serializer_class = ActionSerializer
    filterset_class = ActionFilter
    action_service = ActionService()

    def get_queryset(self, **kwargs):
        queryset = self.action_service.all(**kwargs)
        filtered_queryset = self.filterset_class(self.request.GET, queryset=queryset)
        return filtered_queryset.qs

    def get(self, request, *args, **kwargs):
        instances = self.get_queryset(**kwargs)
        serialized = self.serializer_class(instance=instances, many=True)
        return Response(serialized.data, status=status.HTTP_200_OK)
