from rest_framework.pagination import CursorPagination, PageNumberPagination


class PostListPagination(PageNumberPagination):
    page_size = 2
    page_size_query_param = 'page_size'
    max_page_size = 10


class CommentPagination(CursorPagination):
    page_size = 2
    ordering = '-created_at'
