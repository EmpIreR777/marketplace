from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from django.db.models import Count, Min, Max, F
from django.core.cache import cache
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.views import APIView

from .models import OrganizationsVuz, Programs, Faculties, Specialties, Forms
from .serializers import OrganizationVuzListSerializer, OrganizationVuzDetailSerializer, \
    ProgramListSerializer, VuzFiltersSerializer, ProgramFiltersSerializer
from .filters import OrganizationVuzFilter, ProgramFilter
from .swagger_schemas import program_filter_schema, vuz_filters_schema, program_filters_schema
from .filter_services import get_vuz_filters_data


class OrganizationVuzViewSet(ReadOnlyModelViewSet):
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = OrganizationVuzFilter
    ordering_fields = ['name', 'cost', 'calculation_cost']

    def get_queryset(self):
        queryset = OrganizationsVuz.objects.all().select_related(
            'city', 'contact', 'metro', 'subject'
        ).annotate(
            programs_count=Count('programs'),
            calculation_cost=F('calculation_data__cost_min')
        )
        
        for backend in list(self.filter_backends):
            if backend != OrderingFilter:
                queryset = backend().filter_queryset(self.request, queryset, self)
        
        ordering = self.request.query_params.get('ordering')
        min_price = self.request.query_params.get('price_min')
        max_price = self.request.query_params.get('price_max')
        
        if ordering and ('price' in ordering or 'cost' in ordering):
            direction = '-' if ordering.startswith('-') else ''
            queryset = queryset.filter(calculation_data__cost_min__isnull=False).order_by(f'{direction}calculation_cost')
            self.ordering = None
        elif min_price or max_price:
            queryset = queryset.filter(calculation_data__cost_min__isnull=False).order_by('calculation_cost')
            self.ordering = None
        else:
            self.ordering = ['id']
            
        return queryset

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return OrganizationVuzDetailSerializer
        return OrganizationVuzListSerializer
    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({'request': self.request})
        return context

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        
        if not queryset.exists():
            return Response([], status=status.HTTP_200_OK)
            
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @program_filter_schema
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)


class ProgramPagination(LimitOffsetPagination):
    default_limit = 10
    limit_query_param = 'limit'
    offset_query_param = 'offset'
    max_limit = 100


class ProgramViewSet(ReadOnlyModelViewSet):
    permission_classes = [AllowAny]
    serializer_class = ProgramListSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = ProgramFilter
    ordering_fields = ['cost', 'specialty', 'profile']
    ordering = ['cost', 'id']
    pagination_class = ProgramPagination

    def get_queryset(self):
        vuz_id = self.kwargs.get('vuz_id')
        if vuz_id:
            queryset = Programs.objects.filter(
                organization_vuz_id=vuz_id
            ).select_related('faculty', 'specialty', 'form')
            
            ordering = self.request.query_params.get('ordering')
            
            if ordering == 'name':
                self.ordering = None
                return queryset.order_by('specialty__name')
            elif ordering == '-name':
                self.ordering = None
                return queryset.order_by('-specialty__name')
            elif ordering and ('price' in ordering or 'cost' in ordering):
                direction = '-' if ordering.startswith('-') else ''
                queryset = queryset.exclude(cost__isnull=True).order_by(f'{direction}cost')
                self.ordering = None

            return queryset
        return Programs.objects.none()

    def filter_queryset(self, queryset):
        filtered = super().filter_queryset(queryset)
        return filtered

    @program_filter_schema
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        
        if not queryset.exists():
            return Response([], status=status.HTTP_200_OK)
            
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class FiltersForVuzView(APIView):
    permission_classes = [AllowAny]

    @vuz_filters_schema
    def get(self, request, *args, **kwargs):
        self.request = request
        cache_key = f"vuz_filters:{request.GET.urlencode()}"
        cached_data = cache.get(cache_key)

        if cached_data:
            return Response(cached_data)

        vuz_queryset = OrganizationsVuz.objects.all()
        vuz_filter = OrganizationVuzFilter(request.GET, queryset=vuz_queryset)
        filtered_vuz = vuz_filter.qs

        filter_type = request.query_params.get('filter_type', None)
        limit = request.query_params.get('limit', 20)
        offset = request.query_params.get('offset', 0)
        search = request.query_params.get('search', None)
        cities = request.query_params.get('cities', None)

        try:
            limit = int(limit)
            offset = int(offset)
        except (ValueError, TypeError):
            limit = 20
            offset = 0

        filters_data = get_vuz_filters_data(filtered_vuz, filter_type, limit, offset, search, cities)
        serializer = VuzFiltersSerializer(filters_data)
        response = Response(serializer.data)

        if not filter_type:
            cache.set(cache_key, response.data, 600)

        return response
 


class FiltersForProgramsView(APIView):
    permission_classes = [AllowAny]

    @program_filters_schema
    def get(self, request, vuz_id, *args, **kwargs):
        cache_key = f"program_filters:{vuz_id}:{request.GET.urlencode()}"
        cached_data = cache.get(cache_key)

        if cached_data:
            return Response(cached_data)

        filter_type = request.query_params.get('filter_type')
        
        queryset = Programs.objects.filter(organization_vuz_id=vuz_id)
        program_filter = ProgramFilter(request.query_params, queryset=queryset)
        filtered_queryset = program_filter.qs
        
        faculty_data = []
        specialty_data = []
        form_data = []
        
        if not filter_type or filter_type == 'faculty':
            faculty_data = Faculties.objects.filter(
                id__in=filtered_queryset.values_list('faculty_id', flat=True).distinct()
            )
            
        if not filter_type or filter_type == 'specialty':
            specialty_data = Specialties.objects.filter(
                id__in=filtered_queryset.values_list('specialty_id', flat=True).distinct()
            )
            
        if not filter_type or filter_type == 'form':
            form_data = Forms.objects.filter(
                id__in=filtered_queryset.values_list('form_id', flat=True).distinct()
            )

        aggregations = filtered_queryset.aggregate(
            price_min=Min('cost'),
            price_max=Max('cost'),
            duration_min=Min('duration'),
            duration_max=Max('duration'),
            budget_places_min=Min('budget_places'),
            budget_places_max=Max('budget_places'),
            min_commercial_places=Min('commercial_places'),
            max_commercial_places=Max('commercial_places'),
            min_budget_score=Min('budget_score'),
            max_budget_score=Max('budget_score'),
            min_commercial_score=Min('commercial_score'),
            max_commercial_score=Max('commercial_score'),
        )
        
        response_data = {
            'faculty': faculty_data,
            'specialty': specialty_data,
            'form': form_data,
            'total_count': filtered_queryset.count(),
            **aggregations
        }
        
        serializer = ProgramFiltersSerializer(response_data)
        response = Response(serializer.data)
        
        if not filter_type:
            cache.set(cache_key, response.data, 600)
            
        return response

