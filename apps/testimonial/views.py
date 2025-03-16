from rest_framework.generics import ListAPIView
from rest_framework.permissions import AllowAny

from .models import Testimonial
from .serializers import TestimonialSerializer


class TestimonialListAPIView(ListAPIView):
    serializer_class = TestimonialSerializer
    queryset = Testimonial.objects.filter(is_active=True)
    pagination_class = None
    permission_classes = [AllowAny]
