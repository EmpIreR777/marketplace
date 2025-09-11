from django.db.models import Count, Avg, Value, Q
from django.db.models.functions import Coalesce, Round
from django.shortcuts import get_object_or_404
from django.db.models import Prefetch
from django_filters.rest_framework import DjangoFilterBackend
from django.core.cache import cache

from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView

from author.models import Author, AuthorType
from core.filters import OrganizationNameOrdering
from courses.models import (
    Course,
    LearningType,
    ThematicsType,
    CourseFormat,
    CourseLevel,
    LearningReasons,
    AgeCategory,
    School
)
from courses.filter import CourseFilter
from .filter import AuthorFilter, FeedbackFilter
from .models import Feedback
from .permissions import IsCourseOwnerOrReadOnly, IsOwnerOrAdmin
from .serializers import FeedbackBaseSerializer, FeedbackCreateSerializer, FeedbackUpdateSerializer, \
    AuthorFeedbackTopSerializer, CourseWithFeedbacksSerializer, AuthorFiltersSerializer
from .swagger_schemas import order_schema, top_filters_count_schema


def get_verified_authors_queryset():
    return Author.objects.filter(is_active=True).prefetch_related(
        'courses', 'courses__feedbacks'
    ).only('id', 'title', 'logo')


class FeedbackViewSet(ModelViewSet):
    queryset = Feedback.objects.filter(is_approved=True, parent_feedback__isnull=True)
    filter_backends = [DjangoFilterBackend, OrganizationNameOrdering]
    filterset_class = FeedbackFilter
    ordering = ['-feedback_date']
    ordering_fields = ['feedback_author', 'feedback_to_course', 'feedback_date']
    http_method_names = ["get", "patch", "delete", 'post']

    def get_serializer_class(self):
        if self.action == 'list':
            return FeedbackBaseSerializer
        elif self.action == 'create':
            return FeedbackCreateSerializer
        elif self.action == 'partial_update':
            return FeedbackUpdateSerializer
        return FeedbackBaseSerializer

    def get_permissions(self):
        if self.action == "create":
            return [IsAuthenticated()]
        elif self.action in ("update", "partial_update", "destroy"):
            return [IsOwnerOrAdmin()]
        return [IsCourseOwnerOrReadOnly()]

    def perform_create(self, serializer):
        """Set author before saving"""
        serializer.save(feedback_author=self.request.user)

    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @action(detail=False, methods=['get'],
            permission_classes=[IsAuthenticated],
            url_path='author-feedbacks/(?P<author_id>\d+)')
    def author_feedbacks(self, request, author_id=None):
        author = get_object_or_404(Author, id=author_id)

        if not hasattr(request.user, 'author'):
            return Response({'detail': 'Вы не являетесь автором.'}, status=status.HTTP_403_FORBIDDEN)

        if request.user.author.id == author.id:
            author_courses = author.courses.prefetch_related(
                Prefetch('feedbacks', queryset=Feedback.objects.all())
            )
        else:
            author_courses = author.courses.prefetch_related(
                Prefetch('feedbacks', queryset=Feedback.objects.filter(is_approved=True))
            )

        serializer = CourseWithFeedbacksSerializer(author_courses, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class AuthorTopByFeedbacksViewSet(ReadOnlyModelViewSet):
    queryset = get_verified_authors_queryset()
    serializer_class = AuthorFeedbackTopSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = AuthorFilter

    def get_annotated_queryset(self):
        qs = self.queryset.annotate(
            total_feedbacks=Count('courses__feedbacks', distinct=True),
            total_rating=Round(
                Coalesce(
                    Avg('courses__feedbacks__feedback_rating'),
                    Value(0.0)
                ),
                2
            )
        )
        return qs

    def get_queryset(self):
        if self.action in ('list', 'retrieve'):
            qs = self.get_annotated_queryset()
            ordering = self.request.query_params.get('ordering', '-total_rating,-total_feedbacks')
            return qs.order_by(*ordering.split(','))

        return self.queryset

    @order_schema
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        if not queryset.exists():
            return Response([], status=status.HTTP_200_OK)

        return super().list(request, *args, **kwargs)


class FiltersForAuthorsView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        authors_queryset = get_verified_authors_queryset()
        author_filter = AuthorFilter(request.GET, queryset=authors_queryset)
        filtered_authors = author_filter.qs

        if not filtered_authors.exists():
            filtered_authors = authors_queryset
        
        filters_data = {
            "courses_thematics": ThematicsType.objects.filter(
                courses__author__in=filtered_authors
            ).distinct(),
            "course_formats": CourseFormat.objects.filter(
                course__author__in=filtered_authors
            ).distinct(),
            "course_levels": CourseLevel.objects.filter(
                course__author__in=filtered_authors
            ).distinct(),
            "course_targets": LearningReasons.objects.filter(
                course__author__in=filtered_authors
            ).distinct(),
            "learning_types": LearningType.objects.filter(
                course__author__in=filtered_authors
            ).distinct(),
            "age_category": AgeCategory.objects.filter(
                course__author__in=filtered_authors
            ).distinct(),
            "author_types": [
                {
                    'name': type_value,
                    'translations': dict(AuthorType.choices)[type_value]
                }
                for type_value in filtered_authors.exclude(
                    author_type__isnull=True
                ).values_list('author_type', flat=True).distinct()
                if type_value in dict(AuthorType.choices)
            ]
        }
        
        serializer = AuthorFiltersSerializer(filters_data)
        return Response(serializer.data)


class FeedbackTopFiltersCountView(APIView):
    permission_classes = [AllowAny]
    
    @top_filters_count_schema
    def get(self, request, *args, **kwargs):
        base_authors = get_verified_authors_queryset()
        request_params = request.GET.copy()
        
        courses_thematics = request_params.get('courses_thematics', '').split(',')
        courses_thematics = [theme for theme in courses_thematics if theme]
        has_only_top = len(request_params) == 1 and 'top' in request_params
        
        if 'top' in request_params:
            del request_params['top']
        
        author_filter = AuthorFilter(request.GET, queryset=base_authors)
        filtered_authors = author_filter.qs
        
        filtered_authors = filtered_authors.annotate(
            total_feedbacks=Count('courses__feedbacks', distinct=True),
            total_rating=Round(
                Coalesce(
                    Avg('courses__feedbacks__feedback_rating'),
                    Value(0.0)
                ),
                2
            )
        )
        
        filtered_authors = filtered_authors.order_by('-total_rating', '-total_feedbacks')
        
        if has_only_top:
            filtered_authors = base_authors
        
        filters_map = {
            'master': Q(courses__description__icontains='мастер') | Q(courses__name__icontains='мастер'),
            'language': Q(courses__learning_types__name='typeLanguage'),
            'offline': Q(courses__course_formats__name='offline'),
            'online': Q(courses__course_formats__name='online') | Q(courses__course_formats__name='record'),
            'university': Q(courses__description__icontains='вуз') | Q(courses__description__icontains='универ'),
            'training': Q(courses__description__icontains='тренинг') | Q(courses__name__icontains='тренинг')
        }
        
        response_data = {}
        
        for filter_name, filter_query in filters_map.items():
            author_count = filtered_authors.filter(filter_query).distinct().count()
            response_data[filter_name] = author_count
        
        school_authors = filtered_authors.filter(
            courses__in=School.objects.all()
        ).distinct()
        
        response_data['school'] = school_authors.count()
        response_data['total_filtered_authors'] = filtered_authors.count()
        response_data['total_authors'] = Author.objects.filter(is_active=True).count()
        
        return Response(response_data)
