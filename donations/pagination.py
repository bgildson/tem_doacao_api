from rest_framework.pagination import CursorPagination


class DonationsPagination(CursorPagination):
    page_size = 20
    page_size_query_param = 'page_size'
