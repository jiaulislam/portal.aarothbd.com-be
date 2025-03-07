from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated

from ..models import ProductImage
from ..serializers import ProductImageSerializer


class ProductImageCreateAPIView(CreateAPIView):
    serializer_class = ProductImageSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return ProductImage.objects.all()
