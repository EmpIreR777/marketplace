from typing import Optional
from uuid import UUID
import logging

from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from django.db import models

from rest_framework.viewsets import ModelViewSet
from rest_framework.exceptions import APIException, ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status

from author.models import Author
from courses.filter import CourseFilter
from student.filter import StudentCourseFilter
from courses.models import Course
from courses.serializers import CourseDetailSerializer
from student.serializers import DeleteStudentSerializer, StudentOrderCoursesSerializer, \
    StudentSerializer, StudentUpdateSerializer, StudentScheduleSerializer, PaymentSerializer
from student.models import Student, StudentCoursePurchase
from student.services import StudentRepository
from .filters import StudentCourseScheduleFilter
from courses.models import LearningType, ThematicsType, CourseFormat, CourseLevel, \
    LearningReasons, AgeCategory
from courses.filters_serializers import CourseTypesSerializer

from .schema_swagger import student_schedule_schema, student_bought_courses_schema

logger = logging.getLogger(__name__)

class StudentViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    http_method_names = ["get", "patch", "post", "delete"]
    filter_backends = [DjangoFilterBackend]

    def get_queryset(self):
        if self.request.user.is_staff:
            return Student.objects.all()
        return Student.objects.filter(id=self.request.user.id)

    def get_serializer(self, *args, **kwargs):
        if self.action == 'create_payment':
            return PaymentSerializer(*args, **kwargs)
        return super().get_serializer(*args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
        except APIException:
            return Response({"error": "User profile not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        if not queryset:
            return Response([], status=status.HTTP_204_NO_CONTENT)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()

        if request.user.id != instance.id and not request.user.is_staff:
            logger.warning('user',request.user)
            logger.warning('instance', instance)
            logger.warning('user == instance', request.user == instance)
            return Response({"error": "You do not have permission to update this profile."},
                            status=status.HTTP_403_FORBIDDEN)

        serializer = StudentUpdateSerializer(instance, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @student_bought_courses_schema
    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated], url_path='purchased-courses')
    def get_student_bought_courses(self, request):
        student = getattr(request.user, 'student', None)
        if not student:
            return Response({"error": "This user is not a student"}, status=status.HTTP_400_BAD_REQUEST)

        ordering = request.query_params.get('ordering', 'course__price')
        student_purchases = StudentCoursePurchase.objects.filter(student=student)
        purchased_course_ids = student_purchases.values_list('course_id', flat=True)

        filtered_courses = CourseFilter(
            request.GET, 
            queryset=Course.objects.filter(id__in=purchased_course_ids)
        ).qs

        student_purchases = student_purchases.filter(
            course__in=filtered_courses
        ).select_related('course').order_by(ordering)

        page = self.paginate_queryset(student_purchases)
        if page:
            serializer = StudentOrderCoursesSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = StudentOrderCoursesSerializer(student_purchases, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated], url_path='purchased-courses/(?P<pk>[0-9a-f-]+)')
    def get_student_bought_course(self, request, pk: Optional[UUID] = None):
        if not request.user.is_authenticated:
            return Response({"error": "You are not authenticated"}, status=status.HTTP_401_UNAUTHORIZED)

        student = getattr(request.user, 'student', None)
        if not student:
            return Response({"error": "This user is not a student"},
                            status=status.HTTP_400_BAD_REQUEST)

        try:
            student_purchase = StudentRepository.get_student_purchase(student, pk)
        except StudentCoursePurchase.DoesNotExist:
            return Response({"error": "Course not found"}, status=status.HTTP_404_NOT_FOUND)

        course = student_purchase.course
        serializer = CourseDetailSerializer(course, context={'request': request, 'is_bought': True})

        return Response(serializer.data)

    @action(detail=False, methods=["delete"], url_path="delete")
    def delete_profile(self, request, *args, **kwargs):
        serializer = DeleteStudentSerializer(data=request.data)
        if serializer.is_valid():
            account = StudentRepository.get_student_by_user(request.user)

            password = request.data.get("password")
            if not request.user.check_password(password):
                return Response({"error": "Incorrect password."}, status=status.HTTP_400_BAD_REQUEST)

            reason = serializer.validated_data['reason']
            StudentRepository.delete_student(account, reason)

            return Response({"detail": "Student is deleted and user logged out."},
                            status=status.HTTP_204_NO_CONTENT)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=["post"], permission_classes=[IsAuthenticated], url_path="pay-course")
    def create_payment(self, request):
        student = get_object_or_404(Student, user=request.user)
        course = get_object_or_404(Course, id=request.data["course_id"])

        if not student:
            return Response({"error": "User is not a student"}, status=status.HTTP_403_FORBIDDEN)

        serializer = PaymentSerializer(data=request.data)
        if serializer.is_valid():
            payment_status = serializer.validated_data["payment_status"]

            try:
                purchase = StudentRepository.process_payment(student, course, payment_status)
                return Response({"detail": "Payment successful, course purchased.",
                                 "purchase_id": purchase.id},
                                status=status.HTTP_201_CREATED)
            except ValidationError as e:
                return Response(e.detail, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        if not request.user.is_staff or not request.user.is_superuser:
            return Response({"error": "Permission denied."}, status=status.HTTP_403_FORBIDDEN)

        account = get_object_or_404(Student, id=kwargs['pk'])
        StudentRepository.delete_student(account, reason="Deleted by admin")

        return Response({"detail": "Student is deleted and user logged out."},
                        status=status.HTTP_204_NO_CONTENT)

    @student_schedule_schema
    @action(detail=False, methods=['get'], url_path="get-student-schedule")
    def get_student_schedule(self, request):
        try:
            student = request.user.student
            courses = StudentCoursePurchase.objects.filter(student=student).select_related('course')
        except StudentCoursePurchase.DoesNotExist:
            raise APIException("Student course purchase not found")
        except Student.DoesNotExist:
            raise APIException("Student not found")
        filterset = StudentCourseScheduleFilter(request.GET, queryset=courses)
        if not filterset.is_valid():
            raise APIException("Invalid filter parameter")
        serializer = StudentScheduleSerializer(filterset.qs, many=True)
        return Response(serializer.data)
    
    @action(detail=False, 
            methods=['get'], 
            permission_classes=[IsAuthenticated], 
            url_path='purchased-courses-filters')
    def get_student_purchased_courses_filters(self, request):
        student = getattr(request.user, 'student', None)
        if not student:
            return Response({"error": "This user is not a student"}, status=status.HTTP_400_BAD_REQUEST)

        purchased_courses = Course.objects.filter(purchases__student=student)
        f = LearningType.objects.filter(course__in=purchased_courses).distinct()

        filters_data = {
            "learning_types": LearningType.objects.filter(course__in=purchased_courses).distinct(),
            "courses_thematics": ThematicsType.objects.filter(courses__in=purchased_courses).distinct(),
            "course_formats": CourseFormat.objects.filter(course__in=purchased_courses).distinct(),
            "course_levels": CourseLevel.objects.filter(course__in=purchased_courses).distinct(),
            "course_targets": LearningReasons.objects.filter(course__in=purchased_courses).distinct(),
            "age_category": AgeCategory.objects.filter(course__in=purchased_courses).distinct(),
            "price": {
                "price_min": purchased_courses.aggregate(min_price=models.Min('price'))['min_price'] or 0,
                "price_max": purchased_courses.aggregate(max_price=models.Max('price'))['max_price'] or 0
            },
            "author_types": Author.objects.filter(course__in=purchased_courses).distinct()
        }

        serializer = CourseTypesSerializer(filters_data)
        return Response(serializer.data)
