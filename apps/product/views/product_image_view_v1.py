import logging
import os

from rest_framework.generics import CreateAPIView, DestroyAPIView
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.permissions import IsAuthenticated

from ..models import ProductImage
from ..serializers import ProductImageSerializer

# Initialize logger for this module
logger = logging.getLogger(__name__)


class ProductImageCreateAPIView(CreateAPIView):
    """
    API view for creating product images.

    This view handles the creation of new product images with file upload support.
    It accepts multipart form data and requires user authentication.

    Permissions:
        - User must be authenticated

    Supported formats:
        - Multipart form data
        - Form data

    Expected fields:
        - product: Foreign key to Product model
        - image: Image file to upload
        - is_default: Boolean indicating if this is the default image
        - sale_order: Optional foreign key to PaikarSaleOrder
    """

    serializer_class = ProductImageSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def get_queryset(self):
        """
        Return the queryset for this view.

        Returns:
            QuerySet: All ProductImage objects
        """
        return ProductImage.objects.all()


class ProductImageDeleteAPIView(DestroyAPIView):
    """
    API view for deleting product images.

    This view handles the deletion of product images along with their associated
    physical image files from the storage system. It provides safe file cleanup
    and proper error handling.

    Features:
        - Deletes both database record and physical image file
        - Comprehensive error handling and logging
        - Authentication required
        - Uses 'id' as lookup field
        - Audit trail through logging

    Permissions:
        - User must be authenticated

    URL Pattern:
        - Expected to be used with an 'id' parameter in the URL

    Security:
        - Only authenticated users can delete images
        - File system operations are wrapped with error handling
        - Logs all deletion attempts for audit purposes
    """

    serializer_class = ProductImageSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = "id"

    def get_queryset(self):
        """
        Return the base queryset for this view.

        Note: Django REST Framework automatically filters this queryset
        based on the lookup_field, so we return all objects here.

        Returns:
            QuerySet: All ProductImage objects
        """
        return ProductImage.objects.all()

    def perform_destroy(self, instance) -> None:
        """
        Custom deletion logic that handles both database and file system cleanup.

        This method is automatically called by DRF's DestroyAPIView when a
        DELETE request is processed. It ensures that both the database record
        and the associated image file are properly removed.

        Args:
            instance (ProductImage): The ProductImage instance to be deleted

        Raises:
            OSError: If there's an issue accessing or deleting the file

        Side Effects:
            - Deletes the physical image file from storage
            - Removes the database record
            - Logs the deletion operation
        """
        image_path = None

        try:
            # Store image path for logging before deletion
            if instance.image:
                image_path = instance.image.path

            # Log the deletion attempt
            logger.info(
                f"Attempting to delete ProductImage with ID: {instance.pk}, "
                f"Product: {instance.product.name if instance.product else 'Unknown'}, "
                f"Image path: {image_path or 'No image'}"
            )

            # Check if image file exists and delete it safely
            if instance.image and hasattr(instance.image, "path"):
                try:
                    # Verify file exists before attempting deletion
                    if os.path.isfile(instance.image.path):
                        os.remove(instance.image.path)
                        logger.info(f"Successfully deleted image file: {instance.image.path}")
                    else:
                        logger.warning(f"Image file not found in filesystem: {instance.image.path}")

                except OSError as e:
                    # Log file deletion error but don't prevent database deletion
                    logger.error(
                        f"Failed to delete image file {instance.image.path}: {str(e)}. "
                        "Proceeding with database deletion."
                    )
                except Exception as e:
                    # Catch any other unexpected file-related errors
                    logger.error(
                        f"Unexpected error while deleting image file {instance.image.path}: {str(e)}. "
                        "Proceeding with database deletion."
                    )

            # Delete the database record
            instance.delete()

            # Log successful deletion
            logger.info(
                f"Successfully deleted ProductImage with ID: {instance.pk}, Image path: {image_path or 'No image'}"
            )

        except Exception as e:
            # Log any unexpected errors during the deletion process
            logger.error(f"Failed to delete ProductImage with ID: {instance.pk}. Error: {str(e)}")
            # Re-raise the exception to let DRF handle the error response
            raise
