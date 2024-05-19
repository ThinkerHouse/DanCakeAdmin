from django.db.models import Q

class BasicQueryParamsFilterMixin:
    """
    Mixin to filter queryset based on query parameters.
    """
    def filter_queryset(self, queryset, **kwargs):
        """
        Filter the queryset based on query parameters.

        :param queryset: The queryset to filter.
        :param kwargs: Keyword arguments where keys are field names and values are the query parameter values.
        :return: Filtered queryset.
        """
        if self.request:
            query_params = self.request.query_params
            q_objects = Q()

            # Build Q objects for each query parameter
            for field_name, value in kwargs.items():
                param_value = query_params.get(field_name)
                if param_value:
                    q_objects &= Q(**{f"{field_name}__icontains": param_value})

            # Apply filtering
            if q_objects:
                queryset = queryset.filter(q_objects)

        return queryset
