from rest_framework.generics import ListCreateAPIView
from rest_framework.permissions import DjangoModelPermissions

from .models import UoM, UoMCategory
from .serializers import UoMCategorySerializer, UoMSerializer


class UoMCategoryListCreateAPIView(ListCreateAPIView):
    serializer_class = UoMCategorySerializer
    queryset = UoMCategory.objects.all()
    permission_classes = [DjangoModelPermissions]


class UoMListCreateAPIView(ListCreateAPIView):
    serializer_class = UoMSerializer
    queryset = UoM.objects.all()
    permission_classes = [DjangoModelPermissions]
