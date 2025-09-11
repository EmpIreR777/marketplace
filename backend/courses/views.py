import logging

from django.db.models import Min, Max, Q, DecimalField
from django.db.models.functions import Coalesce
from django.shortcuts import get_object_or_404
from django.utils.timezone import now
from django_filters.rest_framework import DjangoFilterBackend

from drf_yasg.utils import swagger_auto_schema

from rest_framework import status
from rest_framework.decorators import action
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.exceptions import APIException

from author.models import Author, AuthorType
from courses.services import AuthorService, get_similar_courses, get_top_courses
from core.filters import OrganizationNameOrdering
from courses.filter import CourseFilter
from courses.filters_serializers import CourseTypesSerializer
from courses.models import (
    AgeCategory,
    Course,
    ErrorReport,
    LearningType,
    ThematicsType,
    CourseFormat,
    CourseLevel,
    LearningReasons, CourseImage, AdditionalDocument, School
)
from courses.schemas_swagger import (
    unmoderated_courses_schema,
    my_courses_schema,
    moderate_course_schema,
    my_courses_update_schema, similar_courses_schema,
    filters_for_courses_schema,
    course_list_schema,
    author_courses_filters_schema,
    top_filters_count_schema,
)
from courses.serializers import (
    CourseBaseSerializer,
    CourseErrorSerializer,
    CourseOutSerializer,
    CourseCreateSerializer,
    CourseDetailSerializer,
    CourseSerializer,
    CourseListSerializer,
    MainPageStatisticSerializer,
)
from courses.filters_serializers import ThematicsTypeSerializer
from student.models import Student, StudentCoursePurchase
from django.utils.translation import gettext_lazy as _
from vuz.models import OrganizationsVuz

logger = logging.getLogger(__name__)


class CourseViewSet(ModelViewSet):
    filter_backends = [DjangoFilterBackend, OrganizationNameOrdering]
    filterset_class = CourseFilter
    parser_classes = [MultiPartParser, FormParser, JSONParser]
    http_method_names = ["get", "patch", "delete", "post"]
    ordering_fields = ['name', 'price', 'organization', 'date_start']
    ordering = ['name']
    lookup_field = 'id'

    def get_queryset(self):
        user = self.request.user
        today = now().date()
        if self.action == "my_courses" and user.is_authenticated:
            author = AuthorService.get_author_or_organization_or_none(user)
            if not author:
                raise APIException("This user is not an author.")
            return Course.objects.filter(author=author)

        if self.action == "unmoderated_courses" and user.is_staff:
            return Course.objects.filter(is_moderated=False)
        if self.action == "retrieve":
            return Course.objects.all()
        if self.action == "list":
            return Course.objects.filter(is_moderated=True, is_active=True, author__is_active=True)
        return Course.objects.filter(is_moderated=True, is_active=True, author__is_active=True).filter(
            Q(date_end__gte=today) | Q(date_end__isnull=True)
        )

    def get_serializer_class(self):
        if self.action == 'list':
            return CourseListSerializer
        if self.action in ['list', 'unmoderated_courses']:
            return CourseSerializer
        elif self.action in ['create', 'update', 'partial_update']:
            return CourseCreateSerializer
        elif self.action in ['retrieve']:
            return CourseDetailSerializer
        return CourseBaseSerializer

    def create(self, request, *args, **kwargs):
        author = AuthorService.get_author_or_organization_or_none(request.user)
        
        if not author or not author.is_verified:
            return Response("Автор не прошел верификацию для создания курсов.", 
                            status=status.HTTP_403_FORBIDDEN) 
        course_images = request.FILES.getlist("images")
        logger.warning(f"POST data: {request.data}")
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        course = serializer.instance
        if course_images:
            CourseImage.objects.bulk_create([CourseImage(course=course, image=img) for img in course_images])
        return Response(CourseDetailSerializer(course).data, status=status.HTTP_201_CREATED)

    @course_list_schema
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        price_min = request.GET.get('price_min')
        price_max = request.GET.get('price_max')
        ordering = request.GET.get('ordering')
        author_id = request.GET.get('author_id')

        if price_min is not None:
            try:
                price_min = float(price_min)
            except ValueError:
                price_min = None
        # if (price_min is not None and price_max is not None and price_min > 0) or (
        #         price_min is None and price_max is not None):
        #     if not ordering:
        #         queryset = queryset.order_by('price')

        if (price_min is not None or price_max is not None) and not ordering:
            queryset = queryset.order_by('price')
            
        if author_id:
            queryset = queryset.filter(author_id=author_id)
        if not queryset:
            return Response({"count": 0,
                             "next": None,
                             "previous": None,
                             "results": []}, status=status.HTTP_200_OK)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


    def retrieve(self, request, *args, **kwargs):
        course_id = self.kwargs.get('id')
        if not course_id:
            raise APIException("Course ID is required.")
        course = get_object_or_404(Course, id=course_id)

        if not course.is_moderated or not course.is_active:
            if request.user.is_authenticated:
                student = Student.objects.filter(id=request.user.id).first()
                is_my_course = (
                    course.author.id == request.user.id
                    or (student and course in student.bought_courses.all())
                )
                if not is_my_course:
                    return Response(data={'error': 'Course not moderated or not active'},
                                    status=status.HTTP_404_NOT_FOUND)

        student = Student.objects.filter(id=request.user.id).first()
        context = {"request": request}
        
        if student:
            logger.warning(f'student_courses: {student.bought_courses.all()}')
            is_bought = course in student.bought_courses.all()
            context.update({"is_bought": is_bought})
        serializer = self.get_serializer(course, context=context)
        return Response(serializer.data)

    def perform_create(self, serializer):
        organization = serializer.validated_data.get('organization')

        if not organization:
            author = Author.objects.filter(id=self.request.user.id).first()
            if not author:
                raise APIException("This user is not an author.")
            serializer.save(author=author)
        else:
            serializer.save()

    @my_courses_schema
    @action(
        detail=False,
        methods=['get'],
        permission_classes=[IsAuthenticated]
    )
    def my_courses(self, request):
        if request.user.is_anonymous:
            return Response({"detail": "You are not authenticated."}, status=401)

        queryset = self.filter_queryset(self.get_queryset())

        if not queryset.exists():
            return Response({
                "count": 0,
                "next": None,
                "previous": None,
                "results": []
            }, status=status.HTTP_200_OK)
            
        ordering = request.GET.get('ordering', 'price')
        queryset = queryset.order_by(ordering)
        
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = CourseOutSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = CourseOutSerializer(queryset, many=True)
        return Response(serializer.data)

    @my_courses_update_schema
    @action(
        detail=False,
        methods=['patch'],
        permission_classes=[IsAuthenticated],
        url_path='my_courses/update/(?P<id>[^/.]+)'
    )
    def update_my_course(self, request, id=None):
        data = request.data
        try:
            author = Author.objects.get(id=request.user.id)
            course = Course.objects.get(id=id, author=author)
        except Course.DoesNotExist:
            return Response({"detail": "Course not found or you don't have permission to edit it."},
                            status=status.HTTP_404_NOT_FOUND)

        logger.warning(f"data {data}")
        course_images = request.FILES.getlist("images")
        additional_materials = request.FILES.getlist('additional_materials')
        serializer = CourseCreateSerializer(course, data=data, partial=True, context={'request': request})
        if serializer.is_valid():
            serializer.save()
        else:
            logger.error(f"Ошибка валидации: {serializer.errors}")
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        logger.warning(f"images {course_images}")
        if course_images:
            course.images.all().delete()
            CourseImage.objects.bulk_create([CourseImage(course=course, image=img) for img in course_images])
        if additional_materials:
            course.additional_materials.all().delete()
            AdditionalDocument.objects.bulk_create(
                [AdditionalDocument(course=course, file=doc) for doc in additional_materials])
        return Response(serializer.data)

    @unmoderated_courses_schema
    @action(
        detail=False,
        methods=['get'],
        permission_classes=[IsAuthenticated, IsAdminUser],
        url_path='unmoderated'
    )
    def unmoderated_courses(self, request):
        if not request.user.is_staff:
            return Response({"detail": "Permission denied."}, status=status.HTTP_403_FORBIDDEN)

        courses = self.get_queryset()
        page = self.paginate_queryset(courses)
        if page is not None:
            serializer = CourseOutSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = CourseOutSerializer(courses, many=True)
        return Response(serializer.data)

    @similar_courses_schema
    @action(
        detail=True,
        methods=['get'],
        url_path='similar_courses',
    )
    def get_similar_courses(self, request, id):
        """
        Endpoint to get similar courses or if not found return top courses
        """
        try:
            course = Course.objects.get(id=id)
        except Course.DoesNotExist:
            data = {'detail': 'Top courses'}
            courses_to_show = get_top_courses(request, limit=5)
        else:
            data = {'detail': 'Similar courses'}
            courses_to_show = get_similar_courses(course=course, limit=5)
        similar_serializer = CourseSerializer(courses_to_show, many=True, context={"request": request})
        data['courses'] = similar_serializer.data
        return Response(data=data, status=status.HTTP_200_OK)

    @moderate_course_schema
    @action(
        detail=True,
        methods=['get', 'patch'],
        permission_classes=[IsAuthenticated, IsAdminUser],
        url_path='moderate'
    )
    def moderate_course(self, request, id=None):
        try:
            course = Course.objects.get(id=id)
        except Course.DoesNotExist:
            return Response({"detail": "Course not found."}, status=status.HTTP_404_NOT_FOUND)
        serializer = CourseBaseSerializer(course, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @top_filters_count_schema
    @action(
        detail=False,
        methods=['get'],
        url_path='top-filters-count'
    )
    def get_top_filters_count(self, request):
        base_queryset = Course.objects.filter(is_moderated=True, is_active=True, author__is_active=True)
        request_params = request.GET.copy()
        top_param = request_params.get('top', '').lower()
        
        if 'top' in request_params:
            del request_params['top']
        
        only_top_filter = len([k for k in request_params.keys() if not k.startswith('_')]) == 0
        course_filter = CourseFilter(request.GET, queryset=base_queryset)
        filtered_queryset = course_filter.qs
        
        count_queryset = base_queryset if only_top_filter else filtered_queryset
        
        filters_map = {
            'master': Q(description__icontains='мастер') | Q(name__icontains='мастер'),
            'language': Q(learning_types__name='typeLanguage'),
            'offline': Q(course_formats__name='offline'),
            'online': Q(course_formats__name='online') | Q(course_formats__name='record'),
            'university': Q(description__icontains='вуз') | Q(description__icontains='универ'),
            'training': Q(description__icontains='тренинг') | Q(name__icontains='тренинг')
        }

        response_data = {}
        for filter_name, filter_query in filters_map.items():
            response_data[filter_name] = count_queryset.filter(filter_query).distinct().count()

        if top_param == 'school':
            school_ids = filtered_queryset.values_list('id', flat=True)
            response_data['school'] = School.objects.filter(course_ptr_id__in=school_ids).count()
        else:
            school_ids = count_queryset.values_list('id', flat=True)
            response_data['school'] = School.objects.filter(course_ptr_id__in=school_ids).count()
        
        response_data['total_filtered_courses'] = filtered_queryset.count()
        response_data['total_courses'] = base_queryset.count()

        return Response(response_data)


class FiltersForCoursesView(APIView):
    permission_classes = [AllowAny]

    @filters_for_courses_schema
    def get(self, request, *args, **kwargs):
        self.request = request
        courses_queryset = Course.objects.filter(is_moderated=True, is_active=True, author__is_active=True)
        
        top_param = request.query_params.get('top', '')
        is_school_filter = top_param.lower() == 'school' if top_param else False
        
        if is_school_filter:
            school_ids = School.objects.filter(
                is_moderated=True, 
                is_active=True
            ).values_list('course_ptr_id', flat=True)
            
            courses_queryset = courses_queryset.filter(id__in=school_ids)
            
            request_data = request.GET.copy()
            if 'top' in request_data:
                del request_data['top']
                
            course_filter = CourseFilter(request_data, queryset=courses_queryset)
        else:
            course_filter = CourseFilter(request.GET, queryset=courses_queryset)
            
        filtered_courses = course_filter.qs
        
        return self._get_filters_data(filtered_courses, courses_queryset)

    def _get_filters_data(self, filtered_courses, all_courses=None):
        if not filtered_courses.exists():
            filtered_courses = all_courses or Course.objects.filter(
                is_moderated=True, is_active=True, author__is_active=True)
            
        author_types_values = filtered_courses.exclude(
            author__author_type__isnull=True
        ).values_list('author__author_type', flat=True).distinct()
        author_types = []

        for type_value in author_types_values:
            if type_value in dict(AuthorType.choices):
                author_types.append({
                    'name': type_value,
                    'translations': dict(AuthorType.choices)[type_value]
                })

        filters_data = {
            "courses_thematics": ThematicsType.objects.filter(
                courses__in=filtered_courses
            ).distinct(),
            "course_formats": CourseFormat.objects.filter(
                course__in=filtered_courses
            ).distinct(),
            "course_levels": CourseLevel.objects.filter(
                course__in=filtered_courses
            ).distinct(),
            "course_targets": LearningReasons.objects.filter(
                course__in=filtered_courses
            ).distinct(),
            "learning_types": LearningType.objects.filter(
                course__in=filtered_courses
            ).distinct(),
            "price": Course.objects.aggregate(
                price_min=Coalesce(Min("price"), 0, output_field=DecimalField()),
                price_max=Coalesce(Max("price"), 0, output_field=DecimalField())
            ),
            "age_category": AgeCategory.objects.filter(
                course__in=filtered_courses
            ).distinct(),
            "author_types": author_types
        }
        
        serializer = CourseTypesSerializer(filters_data)
        return Response(serializer.data)


class MyCoursesFiltersView(FiltersForCoursesView):
    permission_classes = [IsAuthenticated]

    @author_courses_filters_schema
    def get(self, request, *args, **kwargs):
        author = Author.objects.filter(id=request.user.id).first()
        student = Student.objects.filter(id=request.user.id).first()

        if author:
            courses = Course.objects.filter(author=author)
        elif student:
            courses = student.bought_courses.all()
        else:
            return Response({
                "error": "Пользователь не является ни автором, ни студентом"
            }, status=status.HTTP_403_FORBIDDEN)

        course_filter = CourseFilter(request.GET, queryset=courses)
        filtered_courses = course_filter.qs
        
        return self._get_filters_data(filtered_courses)


class CourseErrorView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(request_body=CourseErrorSerializer)
    def post(self, request, course_id, *args, **kwargs):
        course = get_object_or_404(Course, id=course_id)
        student = get_object_or_404(Student, id=request.user.id)

        serializer = CourseErrorSerializer(data=request.data, context={'student': student})
        if serializer.is_valid():
            serializer.save(course=course)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, course_id, *args, **kwargs):
        course = get_object_or_404(Course, id=course_id)

        if course.author.id != request.user.id:
            return Response({"error": "Вы не автор этого курса"}, status=status.HTTP_403_FORBIDDEN)

        error_reports = ErrorReport.objects.filter(course=course)
        serializer = CourseErrorSerializer(error_reports, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CourseErrorMarkReadView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, course_id, *args, **kwargs):
        course = get_object_or_404(Course, id=course_id)

        if course.author.id != request.user.id:
            return Response({"error": "Вы не автор этого курса"}, status=status.HTTP_403_FORBIDDEN)

        error_reports = ErrorReport.objects.filter(course=course, is_read=False)
        error_reports.update(is_read=True)

        return Response({"message": "Все ошибки отмечены как прочитанные"}, status=status.HTTP_200_OK)
    
class MainPageStatistic(APIView):
    permission_classes = [AllowAny]
    
    def get(self, request, *args, **kwargs):
        data = {
            "courses": Course.objects.filter(is_active=True, is_moderated=True).count(),
            "students": Student.objects.count(),
            "authors": Author.objects.count(),
            "sales": StudentCoursePurchase.objects.count(),
            "vuz": OrganizationsVuz.objects.count()
        }
        serializer = MainPageStatisticSerializer(data)
        return Response(serializer.data)


class ThematicsTypesView(APIView):
    permission_classes = [AllowAny]
    
    def get(self, request, *args, **kwargs):
        learning_types = request.query_params.getlist('learning_type')
        
        if not learning_types:
            return Response({"message": []}, status=status.HTTP_200_OK)
            
        learning_types_expanded = []
        for lt in learning_types:
            learning_types_expanded.extend(lt.split(','))
            
        learning_types_expanded = list(filter(None, set(learning_types_expanded)))
            
        thematics = ThematicsType.objects.filter(
            learning_type__name__in=learning_types_expanded
        ).values('id', 'name', 'translations')
        
        serializer = ThematicsTypeSerializer(thematics, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
