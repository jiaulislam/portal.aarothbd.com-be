from rest_framework import status
from rest_framework.exceptions import APIException


class SlugAlreadyExistException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "Slug already exists in system. Try new one !"
    default_code = "client_error"
