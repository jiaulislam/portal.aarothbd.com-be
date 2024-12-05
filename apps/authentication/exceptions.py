from rest_framework import status
from rest_framework.exceptions import APIException


class TokenServiceFailureException(APIException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    default_detail = "Failed to create token. Try Again!"
    default_code = "server_error"
