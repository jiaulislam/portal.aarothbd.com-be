from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny

from ..models import Review
from ..serializers import ReviewSerializer

__all__ = ["ReviewCreateAPIView"]


# TODO: Need to implement some kind of rate limiting here
class ReviewCreateAPIView(CreateAPIView):
    serializer_class = ReviewSerializer
    queryset = Review.objects.all()
    permission_classes = [AllowAny]
