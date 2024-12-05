from rest_framework import status
from rest_framework.exceptions import APIException


class MissingSentryRequestParamException(APIException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    default_detail = "Missing the 'request' object in the kwargs."
    default_code = "server_error"
