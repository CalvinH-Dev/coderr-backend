from django.db.models import Q


def get_query_param_values(request, params):
    """
    Extract multiple query parameter values from a request.

    Args:
        request: The HTTP request object containing query parameters.
        params (list): List of parameter names to extract.

    Returns:
        dict: Dictionary mapping parameter names to their values.
            Returns None for parameters that are not present.
    """
    values = {}
    for param in params:
        value = request.query_params.get(param)
        if value:
            values[param] = request.query_params.get(param)
        else:
            values[param] = None

    return values


def filter_creator(queryset, id):
    """
    Filter queryset by creator user ID.

    Args:
        queryset: The Django queryset to filter.
        id: The user ID to filter by. If None, no filtering is applied.

    Returns:
        QuerySet: Filtered queryset containing only items created by the
            specified user, or the original queryset if id is None.
    """
    if id is not None:
        queryset = queryset.filter(user__id=id)
    return queryset


def filter_min_price(queryset, min_price):
    """
    Filter queryset by minimum price.

    Args:
        queryset: The Django queryset to filter.
        min_price: The minimum price threshold. If None, no filtering is applied.

    Returns:
        QuerySet: Filtered queryset containing only items with offers priced
            at or above the minimum price, with duplicates removed, or the
            original queryset if min_price is None.
    """
    if min_price is not None:
        queryset = queryset.filter(offers__price__gte=min_price).distinct()
    return queryset


def filter_max_delivery_time(queryset, max_time):
    """
    Filter queryset by maximum delivery time.

    Args:
        queryset: The Django queryset to filter.
        max_time: The maximum delivery time in days. If None, no filtering
            is applied.

    Returns:
        QuerySet: Filtered queryset containing only items with minimum
            delivery time at or below the maximum, or the original queryset
            if max_time is None.
    """
    if max_time is not None:
        queryset = queryset.filter(min_delivery_time__lte=max_time)
    return queryset


def filter_search(queryset, term):
    """
    Filter queryset by search term in description or title.

    Performs case-insensitive search across description and title fields.

    Args:
        queryset: The Django queryset to filter.
        term (str): The search term to look for. If None, no filtering
            is applied.

    Returns:
        QuerySet: Filtered queryset containing only items where the search
            term appears in description or title, or the original queryset
            if term is None.
    """
    if term is not None:
        queryset = queryset.filter(
            Q(description__icontains=term) | Q(title__icontains=term)
        )
    return queryset


def order_queryset(queryset, term):
    """
    Order queryset based on the specified field.

    Args:
        queryset: The Django queryset to order.
        term (str): The ordering term. Supported values:
            - 'min_price': Order by minimum price (ascending)
            - 'updated_at': Order by update timestamp (descending)
            - Any other value returns the queryset unchanged.

    Returns:
        QuerySet: Ordered queryset or the original queryset if term is
            not recognized.
    """
    if term == "min_price":
        return queryset.order_by("min_price")
    if term == "updated_at":
        return queryset.order_by("-updated_at")
    return queryset
