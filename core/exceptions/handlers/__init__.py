from drf_standardized_errors.handler import ExceptionHandler

from core.exceptions import MissingSentryRequestParamException, SlugAlreadyExistException


class CoreExceptionHandler(ExceptionHandler):
    def convert_known_exceptions(self, exc: Exception) -> Exception:
        if isinstance(exc, SlugAlreadyExistException):
            return SlugAlreadyExistException()
        if isinstance(exc, MissingSentryRequestParamException):
            return MissingSentryRequestParamException()
        else:
            return super().convert_known_exceptions(exc)
