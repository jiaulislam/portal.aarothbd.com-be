import os

from rest_framework.generics import CreateAPIView, DestroyAPIView
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.permissions import IsAuthenticated

from ..models import ProductImage
from ..serializers import ProductImageSerializer


class ProductImageCreateAPIView(CreateAPIView):
    serializer_class = ProductImageSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def get_queryset(self):
        return ProductImage.objects.all()


class ProductImageDeleteAPIView(DestroyAPIView):
    serializer_class = ProductImageSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]
    lookup_field = "id"

    def get_queryset(self):
        return ProductImage.objects.all()

    def perform_destroy(self, instance: ProductImage) -> None:  # type: ignore
        if instance.image and os.path.isfile(instance.image.path):
            os.remove(instance.image.path)
        instance.delete()
