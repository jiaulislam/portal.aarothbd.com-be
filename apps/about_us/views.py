from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from core.request import Request

from .models import AboutUs
from .serializers import AboutUsSerializer


class AboutUsAPIView(APIView):
    serializer_class = AboutUsSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        return AboutUs.objects.all()

    def get(self, request: Request, *args, **kwargs):
        about_us = self.get_queryset().first()
        serializer = self.serializer_class(about_us)
        return Response(serializer.data)
