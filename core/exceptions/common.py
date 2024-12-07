from rest_framework import status
from rest_framework.exceptions import APIException


class CustomException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "Unknown error. Please try again !"
    default_code = "client_error"
