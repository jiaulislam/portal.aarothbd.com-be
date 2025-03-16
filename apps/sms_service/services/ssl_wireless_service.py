from typing import Any, Mapping
from uuid import uuid4

import requests
from rest_framework import status

from core.env import env
from core.exceptions import CustomException
from core.services.sentry_service import capture_exception_sentry


class SSLWirelessService:
    def __init__(self):
        self.base_url = env("SSL_SMS_BASE_URL")
        self.api_token = env("SSL_SMS_API_TOKEN")
        self.sid = "AAROTHBD"
        self.uri = None

    def get_full_url(self) -> str:
        return f"{self.base_url}/{self.uri}"

    def _send_request(self, method="get", data: Mapping[str, Any] | None = None) -> requests.Response:
        if method in ("post", "put", "patch") and not data:
            exc = CustomException(detail="Data is required for post, put, patch method")
            exc.status_code = status.HTTP_400_BAD_REQUEST
            raise exc

        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
        }
        request_url = self.get_full_url()
        try:
            if method == "post":
                response = requests.post(request_url, json=data, headers=headers)
            elif method == "put":
                response = requests.put(request_url, json=data, headers=headers)
            elif method == "patch":
                response = requests.patch(request_url, json=data, headers=headers)
            elif method == "delete":
                response = requests.delete(request_url, headers=headers)
            else:
                response = requests.get(request_url, headers=headers)
            response.raise_for_status()
            return response
        except requests.exceptions.ConnectionError as e:
            capture_exception_sentry(e)
            exc = CustomException(detail="Connection error")
            exc.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
            raise exc
        except requests.HTTPError as e:
            capture_exception_sentry(e)
            exc = CustomException(str(e))
            exc.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
            raise exc

    def _single_sms_data(self, message: str, phone_number: str) -> Mapping[str, str]:
        data = {
            "api_token": self.api_token,
            "sid": self.sid,
            "msisdn": f"88{phone_number}",
            "sms": message,
            "csms_id": str(uuid4()),
        }
        return data

    def send_sms(self, message: str, phone_number: str):
        """
        Send single sms
        """
        self.uri = "api/v3/send-sms"
        data = self._single_sms_data(message, phone_number)
        response = self._send_request("post", data)
        data = response.json()
        if data.get("status") == "FAILED":
            exc = CustomException(detail=data.get("error_message"))
            exc.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
            exc.default_code = "sms_send_failed"
            capture_exception_sentry(exc)
            raise exc
        return response.json()
