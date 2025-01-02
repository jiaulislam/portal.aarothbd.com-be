from rest_framework.pagination import LimitOffsetPagination


class ExtendedLimitOffsetPagination(LimitOffsetPagination):
    max_limit = 1000
    default_limit = 50
