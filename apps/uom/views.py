from rest_framework.generics import ListCreateAPIView
from rest_framework.permissions import IsAuthenticated

from .models import UoM, UoMCategory
from .serializers import UoMCategorySerializer, UoMSerializer


class UoMCategoryListCreateAPIView(ListCreateAPIView):
    serializer_class = UoMCategorySerializer
    queryset = UoMCategory.objects.all()
    permission_classes = [IsAuthenticated]


class UoMListCreateAPIView(ListCreateAPIView):
    serializer_class = UoMSerializer
    queryset = UoM.objects.all()
    permission_classes = [IsAuthenticated]
