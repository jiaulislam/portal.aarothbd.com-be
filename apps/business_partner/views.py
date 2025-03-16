from rest_framework.generics import ListAPIView
from rest_framework.permissions import AllowAny

from .models import BusinessPartner
from .serializers import BusinessPartnerSerializer


class BusinessPartnerListAPIView(ListAPIView):
    queryset = BusinessPartner.objects.filter(is_active=True)
    serializer_class = BusinessPartnerSerializer
    pagination_class = None
    permission_classes = [AllowAny]
