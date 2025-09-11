from rest_framework.filters import OrderingFilter


class OrganizationNameOrdering(OrderingFilter):
    def get_ordering(self, request, queryset, view):
        ordering = super().get_ordering(request, queryset, view)
        if ordering:
            return [
                field if 'organization' in field else field
                for field in ordering
            ]
        return ordering
