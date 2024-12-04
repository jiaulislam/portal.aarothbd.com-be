from drf_standardized_errors.handler import ExceptionHandler

from core.exceptions.slug_exception import SlugAlreadyExistException


class CoreExceptionHandler(ExceptionHandler):
    def convert_known_exceptions(self, exc: Exception) -> Exception:
        if isinstance(exc, SlugAlreadyExistException):
            return SlugAlreadyExistException()
        else:
            return super().convert_known_exceptions(exc)
