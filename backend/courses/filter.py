import django_filters
from django.db.models.aggregates import Avg
from django.db.models.query_utils import Q

from .models import Course, ThematicsType, CourseFormat, CourseLevel, LearningReasons, LearningType, School, AgeCategory
from django_filters import filters


class CourseFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains', label="Название")
    price_min = django_filters.NumberFilter(field_name='price',
                                            lookup_expr='gte',
                                            label="От (руб)")
    price_max = django_filters.NumberFilter(field_name='price',
                                            lookup_expr='lte',
                                            label="До (руб)")
    organization = django_filters.CharFilter(field_name='organization__name',
                                             lookup_expr='icontains',
                                             label="Организация"
                                             )
    author_types = filters.CharFilter(
        field_name='author__author_type',
        lookup_expr='exact',
        label="Тип автора"
    )

    top = filters.CharFilter(method='filter_by_top_category', label="Топ категория")

    age_category = filters.ModelMultipleChoiceFilter(
        field_name='age_category__name',
        queryset=AgeCategory.objects.all(),
        to_field_name='name',
        label="Возрастная категория",
    )

    learning_types = filters.ModelMultipleChoiceFilter(
        field_name='learning_types__name',
        queryset=LearningType.objects.all(),
        to_field_name='name',
        label="Тип обучения",
    )

    courses_thematics = filters.ModelMultipleChoiceFilter(
        field_name='courses_thematics__name',
        queryset=ThematicsType.objects.all(),
        to_field_name='name',
        label="Специализация",
    )

    course_targets = filters.ModelMultipleChoiceFilter(
        field_name='learning_reasons__name',
        queryset=LearningReasons.objects.all(),
        to_field_name='name',
        label="Цели курса",
    )

    course_formats = filters.ModelMultipleChoiceFilter(
        field_name='course_formats__name',
        queryset=CourseFormat.objects.all(),
        to_field_name='name',
        label="Формат обучения",
    )

    organization_type = filters.CharFilter(
        field_name='organization__type',
        lookup_expr='exact',
        label="Тип учебного заведения",
    )

    has_diploma = filters.BooleanFilter(field_name='diploma',
                                        label="Диплом")
    is_top_sale = filters.BooleanFilter(field_name='is_top_sale',
                                        label="Топ продаж")
    duration_min = filters.NumberFilter(field_name='course_duration',
                                        lookup_expr='gte', label="От (мес)")
    duration_max = filters.NumberFilter(field_name='course_duration',
                                        lookup_expr='lte', label="До (мес)")

    course_levels = filters.ModelMultipleChoiceFilter(
        field_name='course_levels__name',
        queryset=CourseLevel.objects.all(),
        to_field_name='name',
        label="Уровень программы",
    )

    minimal_rating = filters.NumberFilter(
        method='filter_minimal_rating',
        label="Минимальный рейтинг",
        min_value=1,
        max_value=5
    )

    def __init__(self, data=None, *args, **kwargs):
        if data is not None:
            data = data.copy()
            for key, value in data.items():
                if isinstance(value, str) and ',' in value:
                    data.setlist(key, value.split(','))
        super().__init__(data, *args, **kwargs)

    class Meta:
        model = Course
        fields = [
            'name', 'price_min', 'price_max',
            'organization', 'courses_thematics', 'course_formats',
            'organization_type', 'has_diploma', 'duration_min',
            'duration_max', 'course_levels', 'is_top_sale', 'learning_types',
            'author_types', 'age_category'
        ]

    def filter_minimal_rating(self, queryset, name, value):
        return queryset.annotate(
            avg_rating=Avg(
                'feedbacks__feedback_rating',
                filter=Q(feedbacks__is_approved=True)
            )
        ).filter(avg_rating__gte=value)

    def filter_by_top_category(self, queryset, name, value):
        if not value:
            return queryset
        
        if value.lower() == 'school':
            return queryset

        filters_map = {
            'master': Q(description__icontains='мастер') | Q(name__icontains='мастер'),
            'language': Q(learning_types__name='typeLanguage'),
            'offline': Q(course_formats__name='offline'),
            'online': Q(course_formats__name='online') | Q(course_formats__name='record'),
            'university': Q(description__icontains='вуз') | Q(description__icontains='универ'),
            'training': Q(description__icontains='тренинг') | Q(name__icontains='тренинг')
        }

        filter_query = filters_map.get(value.lower())
        if filter_query:
            return queryset.filter(filter_query).distinct()
        return queryset
