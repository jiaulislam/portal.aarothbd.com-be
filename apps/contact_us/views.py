from typing import Any

from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response

from .serializers import ContactUsSerializer
from .services import EmailReceipentService


class ContactUsCreateAPIView(CreateAPIView):
    serializer_class = ContactUsSerializer
    permission_classes = [AllowAny]

    def post(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        email_receipent_service = EmailReceipentService()
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()

        email_receipent_service.send_email(
            serializer.data["subject"],
            serializer.data["message"],
        )
        instance.is_mail_sent = True
        instance.save()
        return Response(serializer.data)
