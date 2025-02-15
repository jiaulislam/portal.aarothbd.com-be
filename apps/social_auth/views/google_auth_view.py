from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from core.request import Request

from ..serializers import GoogleAuthLoginSerializer

__all__ = ["GoogleSignInAuthAPIView"]


class GoogleSignInAuthAPIView(GenericAPIView):
    permission_classes = []
    authentication_classes = []
    serializer_class = GoogleAuthLoginSerializer

    def post(self, request: Request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)  # type: ignore
        serializer.is_valid(raise_exception=True)

        return Response({"done": "ok"})
