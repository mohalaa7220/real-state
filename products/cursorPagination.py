from rest_framework.pagination import CursorPagination, LimitOffsetPagination
from rest_framework.pagination import PageNumberPagination

from rest_framework.response import Response


class ProductsPagination(PageNumberPagination):
    page_size = 6
    page_size_query_param = 'page_size'
    max_page_size = 100


class ProductLimitOffsetPagination(LimitOffsetPagination):
    default_limit = 1


class ProductCursorPagination(CursorPagination):
    page_size = 1
    cursor_query_param = 'cursor'
