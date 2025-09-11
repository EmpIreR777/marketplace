import django_filters
from django.db.models import Q, OuterRef, Exists
from django.db.models import JSONField
from .models import OrganizationsVuz, Programs


class OrganizationVuzFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(method='filter_name')
    city = django_filters.CharFilter(field_name='city__name', lookup_expr='icontains')
    subject = django_filters.CharFilter(field_name='subject__name', lookup_expr='icontains')
    metro = django_filters.CharFilter(field_name='metro__name', lookup_expr='icontains')
    organization_type = django_filters.CharFilter(field_name='organization_type', lookup_expr='icontains')
    # rating_min = django_filters.NumberFilter(field_name='rating', lookup_expr='gte')
    # rating_max = django_filters.NumberFilter(field_name='rating', lookup_expr='lte')
    price_min = django_filters.NumberFilter(method='filter_price_min')
    price_max = django_filters.NumberFilter(method='filter_price_max')
    has_hostel = django_filters.BooleanFilter(field_name='is_hostel')
    is_state = django_filters.CharFilter(method='filter_is_state')
    is_military = django_filters.BooleanFilter(field_name='is_military')
    
    faculty = django_filters.CharFilter(method='filter_faculty')
    specialty = django_filters.CharFilter(method='filter_specialty')
    form = django_filters.CharFilter(method='filter_form')
    level_code = django_filters.CharFilter(method='filter_level_code')

    def filter_name(self, queryset, name, value):
        if value:
            return queryset.filter(
                Q(name__icontains=value) |
                Q(full_name__icontains=value) |
                Q(short_name__icontains=value)
            )
        return queryset
    
    def filter_is_state(self, queryset, name, value):
        if value == "Государственный":
            return queryset.filter(is_state=True)
        elif value == "Частный":
            return queryset.filter(is_state=False)
        return queryset
    
    def filter_price_min(self, queryset, name, value):
        if value:
            try:
                float_value = float(value)
                return queryset.filter(calculation_data__cost_min__gte=float_value)
            except (ValueError, TypeError):
                return queryset
        return queryset
    
    def filter_price_max(self, queryset, name, value):
        if value:
            try:
                float_value = float(value)
                return queryset.filter(calculation_data__cost_min__lte=float_value)
            except (ValueError, TypeError):
                return queryset
        return queryset
    
    def filter_faculty(self, queryset, name, value):
        if value:
            faculty_names = [name.strip() for name in value.split(',')]
            
            conditions = Q()
            for faculty_name in faculty_names:
                conditions |= Q(
                    Exists(
                        Programs.objects.filter(
                            organization_vuz=OuterRef('id'),
                            faculty__name__icontains=faculty_name
                        )
                    )
                )
            
            filtered = queryset.filter(conditions)
            return filtered
        return queryset
    
    def filter_specialty(self, queryset, name, value):
        if value:
            specialty_names = [name.strip() for name in value.split(',')]
            
            conditions = Q()
            for specialty_name in specialty_names:
                conditions |= Q(
                    Exists(
                        Programs.objects.filter(
                            organization_vuz=OuterRef('id'),
                            specialty__name__icontains=specialty_name
                        )
                    )
                )
            
            filtered = queryset.filter(conditions)
            return filtered
        return queryset
    
    def filter_form(self, queryset, name, value):
        if value:
            return queryset.filter(
                Exists(
                    Programs.objects.filter(
                        organization_vuz=OuterRef('id'),
                        form__name__icontains=value
                    )
                )
            )
        return queryset

    def filter_level_code(self, queryset, name, value):
        if value:
            return queryset.filter(
                Exists(
                    Programs.objects.filter(
                        organization_vuz=OuterRef('id'),
                        specialty__level_code=value
                    )
                )
            )
        return queryset

    class Meta:
        model = OrganizationsVuz
        fields = [
            'name', 'city', 'subject', 'metro',
            'rating', 'is_hostel', 'is_state', 'is_military'
        ]
        filter_overrides = {
            JSONField: {
                'filter_class': django_filters.CharFilter,
                'extra': lambda f: {
                    'lookup_expr': 'icontains',
                }
            },
        }


class ProgramFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(field_name='profile', lookup_expr='icontains')
    faculty = django_filters.CharFilter(field_name='faculty__name', lookup_expr='icontains')
    specialty = django_filters.CharFilter(field_name='specialty__name', lookup_expr='icontains')
    form = django_filters.CharFilter(field_name='form__name', lookup_expr='icontains')
    budget_places_min = django_filters.NumberFilter(field_name='budget_places', lookup_expr='gte')
    budget_places_max = django_filters.NumberFilter(field_name='budget_places', lookup_expr='lte')
    min_budget_score = django_filters.NumberFilter(field_name='budget_score', lookup_expr='gte')
    max_budget_score = django_filters.NumberFilter(field_name='budget_score', lookup_expr='lte')
    min_commercial_places = django_filters.NumberFilter(field_name='commercial_places', lookup_expr='gte')
    max_commercial_places = django_filters.NumberFilter(field_name='commercial_places', lookup_expr='lte')
    min_commercial_score = django_filters.NumberFilter(field_name='commercial_score', lookup_expr='gte')
    max_commercial_score = django_filters.NumberFilter(field_name='commercial_score', lookup_expr='lte')
    price_min = django_filters.NumberFilter(field_name='cost', lookup_expr='gte')
    price_max = django_filters.NumberFilter(field_name='cost', lookup_expr='lte')
    duration_min = django_filters.NumberFilter(field_name='duration', lookup_expr='gte')
    duration_max = django_filters.NumberFilter(field_name='duration', lookup_expr='lte')
    level_code = django_filters.CharFilter(field_name='specialty__level_code')

    class Meta:
        model = Programs
        fields = [
            'profile', 'faculty', 'specialty', 'form',
            'budget_places', 'budget_score',
            'commercial_places', 'commercial_score',
            'cost', 'duration',
            'specialty__level_code'
        ] 