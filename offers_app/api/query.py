from django.db.models import Q


def get_query_param_values(request, params):
    values = {}
    for param in params:
        values[param] = request.query_params.get(param)

    return values


def filter_creator(queryset, id):
    if id is not None:
        queryset = queryset.filter(user__id=id)
    return queryset


def filter_min_price(queryset, min_price):
    if min_price is not None:
        queryset = queryset.filter(offers__price__gte=min_price).distinct()
    return queryset


def filter_max_delivery_time(queryset, max_time):
    if max_time is not None:
        queryset = queryset.filter(min_delivery_time__lte=max_time)
    return queryset


def filter_search(queryset, term):
    if term is not None:
        queryset = queryset.filter(
            Q(description__icontains=term) | Q(title__icontains=term)
        )
    return queryset


def order_queryset(queryset, term):
    if term == "min_price":
        return queryset.order_by("min_price")
    if term == "updated_at":
        return queryset.order_by("-updated_at")
    return queryset
