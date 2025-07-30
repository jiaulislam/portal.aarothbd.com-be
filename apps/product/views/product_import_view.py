from django.core.files.storage import default_storage
from rest_framework import parsers, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.product.serializers.product_import_serializer import ProductImportFileSerializer
from apps.product.services.product_import_service import ProductImportService
from apps.product.tasks import import_products_from_file


class ProductExcelOrCSVImportAPIView(APIView):
    """
    API view to import products from an uploaded Excel or CSV file.
    Uses a serializer for file validation and handles file processing securely.
    """

    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [parsers.MultiPartParser]

    def post(self, request, format=None):
        serializer = ProductImportFileSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        file = serializer.validated_data["file"]

        # Save file temporarily
        file_path = default_storage.save(f"tmp/{file.name}", file)
        file_full_path = default_storage.path(file_path)

        try:
            # Validate file using the service (header and missing value check)
            validation_error = ProductImportService.validate_file(file_full_path)
            if validation_error:
                default_storage.delete(file_path)
                return Response(validation_error, status=status.HTTP_400_BAD_REQUEST)

            # If all validation passes, trigger Celery task
            import_products_from_file.delay(file_full_path)
            return Response(
                {"message": "Product import started. You will be notified when it is complete."},
                status=status.HTTP_202_ACCEPTED,
            )
        except Exception as e:
            default_storage.delete(file_path)
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
