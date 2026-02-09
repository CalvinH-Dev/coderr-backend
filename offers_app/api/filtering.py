def filter_creator(queryset, id):
    if id is not None:
        queryset = queryset.filter(user__id=id)
    return queryset
