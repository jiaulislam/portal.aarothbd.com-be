from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from core.permissions import IsSuperAdmin

from .filters import ActionFilter
from .serializers import ActionExecuteSerializer, ActionSerializer
from .services import ActionService


class ActionListAPIView(GenericAPIView):
    serializer_class = ActionSerializer
    filterset_class = ActionFilter
    permission_classes = [IsSuperAdmin]
    action_service = ActionService()

    def get_queryset(self, **kwargs):
        queryset = self.action_service.all(**kwargs)
        filtered_queryset = self.filterset_class(self.request.GET, queryset=queryset)
        return filtered_queryset.qs

    def get(self, request, *args, **kwargs):
        data = self.action_service.get_actions_data()
        return Response(data, status=status.HTTP_200_OK)


class ActionExecuteAPIView(GenericAPIView):
    serializer_class = ActionExecuteSerializer
    permission_classes = [IsSuperAdmin]
    action_service = ActionService()

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)  # type: ignore
        serializer.is_valid(raise_exception=True)
        action = serializer.validated_data.get("action_name")
        self.action_service.call_action(action)
        return Response({"detail": "action executed successfully !"}, status=status.HTTP_202_ACCEPTED)
