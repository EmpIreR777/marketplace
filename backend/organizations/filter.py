import django_filters
from .models import Organization


class OrganizationFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains')
    full_name = django_filters.CharFilter(lookup_expr='icontains')
    

    class Meta:
        model = Organization
        fields = ['name', 'full_name']