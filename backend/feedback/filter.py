import django_filters

from .models import Feedback
from django_filters import filters
from django.db.models.functions import Coalesce, Round
from django.db.models import Count, Avg, Value, Q, Subquery, OuterRef, FloatField, Exists, Prefetch
from author.models import Author
from courses.models import (
    Course,
    LearningType,
    CourseLevel,
    CourseFormat,
    ThematicsType,
    LearningReasons,
    AgeCategory
)
from django.core.cache import cache
from functools import lru_cache


class FeedbackFilter(django_filters.FilterSet):
    feedback_to_course = filters.ModelChoiceFilter(
        queryset=Course.objects.all(),
        field_name='feedback_to_course',
        label='Курс'
    )

    class Meta:
        model = Feedback
        fields = ['feedback_to_course']


class AuthorFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(
        field_name='title',
        lookup_expr='icontains',
        label="Название"
    )
    
    top = django_filters.CharFilter(
        method='filter_by_top_category',
        label="Топ категория"
    )
    
    author_types = django_filters.CharFilter(
        field_name='author_type',
        lookup_expr='exact',
        label="Тип автора"
    )
    
    learning_types = django_filters.ModelMultipleChoiceFilter(
        queryset=LearningType.objects.all(),
        method='filter_learning_types',
        to_field_name='name',
        label="Тип обучения"
    )
    
    course_levels = django_filters.ModelMultipleChoiceFilter(
        queryset=CourseLevel.objects.all(),
        method='filter_course_levels',
        to_field_name='name',
        label="Уровень курса"
    )
    
    course_formats = django_filters.ModelMultipleChoiceFilter(
        queryset=CourseFormat.objects.all(),
        method='filter_course_formats',
        to_field_name='name',
        label="Формат курса"
    )
    
    courses_thematics = django_filters.ModelMultipleChoiceFilter(
        queryset=ThematicsType.objects.all(),
        method='filter_courses_thematics',
        to_field_name='name',
        label="Тематика курса"
    )
    
    course_targets = django_filters.ModelMultipleChoiceFilter(
        queryset=LearningReasons.objects.all(),
        method='filter_course_targets',
        to_field_name='name',
        label="Целевая аудитория"
    )
    
    age_category = django_filters.ModelMultipleChoiceFilter(
        queryset=AgeCategory.objects.all(),
        method='filter_age_category',
        to_field_name='name',
        label="Возрастная категория"
    )
    
    min_feedbacks = django_filters.NumberFilter(
        method='filter_min_feedbacks',
        label='Минимальное количество отзывов'
    )
    
    min_rating = django_filters.NumberFilter(
        method='filter_min_rating',
        label='Минимальный рейтинг'
    )

    def filter_learning_types(self, queryset, name, value):
        if not value:
            return queryset
        course_subquery = Course.objects.filter(
            learning_types__name__in=value,
            author=OuterRef('pk')
        )
        return queryset.filter(Exists(course_subquery))

    def filter_course_levels(self, queryset, name, value):
        if not value:
            return queryset
        course_subquery = Course.objects.filter(
            course_levels__name__in=value,
            author=OuterRef('pk')
        )
        return queryset.filter(Exists(course_subquery))

    def filter_course_formats(self, queryset, name, value):
        if not value:
            return queryset
        course_subquery = Course.objects.filter(
            course_formats__name__in=value,
            author=OuterRef('pk')
        )
        return queryset.filter(Exists(course_subquery))

    def filter_courses_thematics(self, queryset, name, value):
        if not value:
            return queryset
        course_subquery = Course.objects.filter(
            courses_thematics__name__in=value,
            author=OuterRef('pk')
        )
        return queryset.filter(Exists(course_subquery))

    def filter_course_targets(self, queryset, name, value):
        if not value:
            return queryset
        course_subquery = Course.objects.filter(
            learning_reasons__name__in=value,
            author=OuterRef('pk')
        )
        return queryset.filter(Exists(course_subquery))

    def filter_age_category(self, queryset, name, value):
        if not value:
            return queryset
        course_subquery = Course.objects.filter(
            age_category__name__in=value,
            author=OuterRef('pk')
        )
        return queryset.filter(Exists(course_subquery))

    def filter_min_feedbacks(self, queryset, name, value):
        feedback_count = Subquery(
            Course.objects.filter(author=OuterRef('pk'))
            .annotate(feedback_count=Count('feedbacks'))
            .values('feedback_count')[:1]
        )
        return queryset.annotate(
            total_feedbacks=Coalesce(feedback_count, 0)
        ).filter(total_feedbacks__gte=value)

    def filter_min_rating(self, queryset, name, value):
        min_value = max(0, float(value))
        
        avg_rating = Subquery(
            Course.objects.filter(author=OuterRef('pk'))
            .annotate(avg_rating=Round(Avg('feedbacks__feedback_rating'), 2))
            .values('avg_rating')[:1],
            output_field=FloatField()
        )
        
        return queryset.annotate(
            total_rating=Coalesce(avg_rating, Value(0.0))
        ).filter(total_rating__gte=min_value, total_rating__lte=4)

    @staticmethod
    @lru_cache(maxsize=128)
    def _get_course_ids_for_category(category):
        cache_key = f'author_filter_course_ids_{category}'
        cached_ids = cache.get(cache_key)
        
        if cached_ids is not None:
            return cached_ids
            
        filters_dict = {
            'school': lambda: Course.objects.filter(school__isnull=False),
            'master': lambda: Course.objects.filter(
                Q(description__icontains='мастер') | Q(name__icontains='мастер')
            ),
            'language': lambda: Course.objects.filter(learning_types__name='typeLanguage'),
            'offline': lambda: Course.objects.filter(course_formats__name='offline'),
            'online': lambda: Course.objects.filter(Q(course_formats__name='online') | Q(course_formats__name='record')),
            'university': lambda: Course.objects.filter(
                Q(description__icontains='вуз') | Q(description__icontains='универ')
            ),
            'training': lambda: Course.objects.filter(
                Q(description__icontains='тренинг') | Q(name__icontains='тренинг')
            )
        }
        
        filter_func = filters_dict.get(category)
        if not filter_func:
            return []
            
        course_ids = list(filter_func().values_list('id', flat=True))
        cache.set(cache_key, course_ids, 60 * 60)
        
        return course_ids

    def filter_by_top_category(self, queryset, name, value):
        if not value:
            return queryset
        
        value = value.lower()
        course_ids = self._get_course_ids_for_category(value)
        
        if not course_ids:
            return queryset
        
        course_subquery = Course.objects.filter(
            id__in=course_ids,
            author=OuterRef('pk')
        )
        return queryset.filter(Exists(course_subquery))

    def filter_queryset(self, queryset):
        if not hasattr(self, 'data') or 'top' not in self.data:
            return super().filter_queryset(queryset)
        
        self.is_valid()
        
        top_value = None
        data = self.data.copy()
        top_value = data.pop('top', None)
        
        original_data = self.data
        self.data = data
        
        try:
            filtered_queryset = super().filter_queryset(queryset)
        except Exception as e:
            self.data = original_data
            raise e
        
        self.data = original_data
        
        if top_value:
            value = top_value[0] if isinstance(top_value, list) else top_value
            filtered_queryset = self.filter_by_top_category(filtered_queryset, 'top', value)
        
        return filtered_queryset

    class Meta:
        model = Author
        fields = ['title', 'author_types']
