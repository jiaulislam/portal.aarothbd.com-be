from rest_framework.generics import CreateAPIView

from ..models import Review
from ..serializers import ReviewSerializer

__all__ = ["ReviewCreateAPIView"]


# TODO: Need to implement some kind of rate limiting here
# TODO: Need to move the review works to the product module
class ReviewCreateAPIView(CreateAPIView):
    serializer_class = ReviewSerializer
    queryset = Review.objects.all()
