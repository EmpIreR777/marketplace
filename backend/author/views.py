import logging
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.exceptions import NotFound

from rest_framework.viewsets import ModelViewSet
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework.decorators import action

from author.models import Author
from author.serializers import AuthorSerializer
from author.schemas_swagger import (
    author_list_schema,
    verify_author_schema,
    retrieve_author_schema,
)
from author.author_filter import AuthorFilter
from author.add_verify_info import update_verify_fields
from feedback.serializers import FeedbackBaseSerializer
from feedback.models import Feedback
from courses.serializers import CourseListSerializer
from courses.models import Course

logger = logging.getLogger(__name__)

class AuthorView(ModelViewSet):
    permission_classes = [IsAuthenticated]
    parser_classes = [FormParser, MultiPartParser, JSONParser]
    filter_backends = [DjangoFilterBackend]
    filterset_class = AuthorFilter
    queryset = Author.objects.none()
    serializer_class = AuthorSerializer
    ordering_fields = ['author_type']
    search_fields = ['name']
    ordering = ['author_type']
    http_method_names = ["get", "patch", "delete"]

    def get_queryset(self):
        if self.request.user.is_staff:
            return Author.objects.all()
        return Author.objects.filter(id=self.request.user.id)

    @author_list_schema
    def list(self, request, *args, **kwargs):
        try:
            return super().list(request, *args, **kwargs)
        except NotFound:
            return Response([], status=status.HTTP_200_OK)

    def partial_update(self, request, *args, **kwargs):
        profile = get_object_or_404(Author, id=kwargs["pk"])
        verify_fields_data = {key.replace("verify_fields[", "").replace("]", ""): value for key, value in request.data.items() if key.startswith("verify_fields")}
        full_data = {
            "author_type": request.data.get("author_type"),
            "verify_fields": verify_fields_data,
            "documents": request.FILES.get("documents")
        }
        logger.warning(f"{request.data = }")
        logger.warning(f"Перед обновлением: {profile.photo = }")
             
        serializer = self.get_serializer(profile, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        update_verify_fields(profile, full_data)
        logger.warning(f"После обновления: {profile.photo = }")
        return Response(serializer.data, status=status.HTTP_200_OK)

    @retrieve_author_schema
    def retrieve(self, request, *args, **kwargs):
        profile = get_object_or_404(Author, id=kwargs["pk"])
        serializer = self.get_serializer(profile)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @verify_author_schema
    @action(detail=True, methods=["patch"], url_path="verify-profile", permission_classes=[IsAdminUser])
    def verify_profile_admin(self, request, pk=None):
        profile = get_object_or_404(Author, id=pk)

        if profile.is_verified:
            return Response({"error": "Профиль уже верифицирован"}, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(profile, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=["get"], url_path="feedbacks", permission_classes=[])
    def get_feedbacks_by_author(self, request, pk=None):
        author = get_object_or_404(Author, id=pk)
        feedbacks = Feedback.objects.filter(feedback_to_course__author=author).order_by('-feedback_date')

        page = self.paginate_queryset(feedbacks)
        if page is not None:
            serializer = FeedbackBaseSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = FeedbackBaseSerializer(feedbacks, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @action(detail=True, methods=["get"], url_path="author-courses", permission_classes=[])
    def get_author_courses(self, request, pk=None):
        author = get_object_or_404(Author, id=pk)

        if not Course.objects.filter(author=author).exists():
            return Response({"detail": "У автора нет курсов."}, status=status.HTTP_404_NOT_FOUND)

        courses = Course.objects.filter(author=author, is_moderated=True, is_active=True, author__is_active=True)
        
        ordering = request.GET.get('ordering', 'price')
        courses = courses.order_by(ordering)

        page = self.paginate_queryset(courses)
        if page is not None:
            serializer = CourseListSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = CourseListSerializer(courses, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
