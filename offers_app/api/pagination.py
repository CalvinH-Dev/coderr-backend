from rest_framework.pagination import PageNumberPagination


class OfferPackageSetPagination(PageNumberPagination):
    """
    Pagination class for offer package listings.

    Provides page-based pagination with a default page size of 6 items.
    Clients can request a custom page size up to a maximum of 10 items
    per page using the 'page_size' query parameter.

    Attributes:
        page_size (int): Default number of items per page (6).
        page_size_query_param (str): Query parameter name for custom page size.
        max_page_size (int): Maximum allowed items per page (10).
    """

    page_size = 6
    page_size_query_param = "page_size"
    max_page_size = 10
