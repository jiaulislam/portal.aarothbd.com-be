from django.contrib.contenttypes.models import ContentType
from rest_framework import status
from rest_framework.generics import ListAPIView, RetrieveAPIView, get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from ..constants import ExcludePermissionModelsList
from ..serializers.content_type_serializer import ContentTypeSerializer
from ..serializers.permission_serializers import PermissionSerializer


class ContentTypeListAPIView(ListAPIView):
    queryset = ContentType.objects.all()
    serializer_class = ContentTypeSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        queryset = ContentType.objects.prefetch_related("permission_set")
        excluded_models_list = list(ExcludePermissionModelsList)
        queryset = queryset.exclude(model__in=excluded_models_list)
        return queryset


class ContentTypePermissionListAPIView(RetrieveAPIView):
    queryset = ContentType.objects.all()
    serializer_class = ContentTypeSerializer
    permission_serializer_class = PermissionSerializer
    permission_classes = (IsAuthenticated,)

    def retrieve(self, request, *args, **kwargs):
        content_type_id = kwargs.get("contenttype_id")
        content_type = get_object_or_404(ContentType, id=content_type_id)
        permissions = content_type.permission_set.all()
        serialized = self.permission_serializer_class(permissions, many=True)  # type: ignore
        return Response(serialized.data, status=status.HTTP_200_OK)
