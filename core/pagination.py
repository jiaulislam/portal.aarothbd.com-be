from rest_framework.pagination import LimitOffsetPagination


class ExtendedLimitOffsetPagination(LimitOffsetPagination):
    max_limit = 99
    default_limit = 10
