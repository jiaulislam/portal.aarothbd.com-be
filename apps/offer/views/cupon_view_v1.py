from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from ..serializers import CuponSerializer, CuponValidateSerializer
from ..services.cupon_service import CuponService


class CuponValidateAPIView(APIView):
    serializer_class = CuponValidateSerializer
    cupon_service = CuponService()
    permission_classes = [AllowAny]

    def get_serializer_class(self):
        if self.request.method == "POST":
            return CuponValidateSerializer
        return CuponSerializer

    def get_serializer(self, *args, **kwargs):
        return self.get_serializer_class()(*args, **kwargs)

    def post(self, request: Request, cupon_code: str, *args, **kwargs) -> Response:
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        total_amount = serializer.validated_data["total_amount"]
        cupon, discount_amount = self.cupon_service.validate_cupon(cupon_code, total_amount)
        response = {
            "id": cupon.pk,
            "cupon_code": cupon.cupon_code,
            "discount_mode": cupon.discount_mode,
            "discount_amount": discount_amount,
            "status": "valid",
        }
        return Response(response, status=status.HTTP_200_OK)
