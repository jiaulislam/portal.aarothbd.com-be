from rest_framework import status
from rest_framework.generics import RetrieveUpdateDestroyAPIView
from rest_framework.response import Response

from .serializers import AddressSerializer
from .services import AddressService


class AddressRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    http_method_names = ["get", "put", "delete"]
    serializer_class = AddressSerializer
    lookup_field = "id"
    service_class = AddressService()

    def get_queryset(self):
        return self.service_class.all()

    def update(self, request, *args, **kwargs):
        instance = self.service_class.get(**kwargs)
        serialized = self.serializer_class(data=request.data)
        serialized.is_valid(raise_exception=True)
        instance = self.service_class.update(instance, serialized.validated_data, request=request)
        return Response(self.serializer_class(instance).data, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        instance = self.service_class.get(**kwargs)
        _ = self.service_class.update_status(instance, False, request=request)
        response = {"detail": "Address successfully deleted"}
        return Response(response, status=status.HTTP_200_OK)
