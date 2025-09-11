from rest_framework import serializers
from django.conf import settings

from author.models import Author
from courses.models import Course, LearningType, ThematicsType, CourseFormat, CourseLevel, LearningReasons, AgeCategory
from core.settings import HOST_URL
from .models import Feedback
from feedback.services import FeedbackService


class FeedbackBaseSerializer(serializers.ModelSerializer):
    time_ago = serializers.SerializerMethodField()
    replies = serializers.SerializerMethodField()
    feedback_author = serializers.SerializerMethodField()
    feedback_to_course = serializers.SerializerMethodField()

    class Meta:
        model = Feedback
        fields = ['id', 'feedback_author', 'feedback_text', 'feedback_rating',
                  'time_ago', 'replies', 'feedback_to_course', 'parent_feedback']

    def get_feedback_author(self, obj):
        return {
            "id": obj.feedback_author.id,
            "first_name": obj.feedback_author.first_name,
            "last_name": obj.feedback_author.last_name,
            "middle_name": obj.feedback_author.middle_name,
            "photo": obj.feedback_author.photo.url if obj.feedback_author.photo else None
        } if obj.feedback_author else None

    def get_feedback_to_course(self, obj):
        if obj.parent_feedback and obj.parent_feedback.feedback_author:
            author = obj.parent_feedback.feedback_author.id
        elif obj.feedback_to_course and obj.feedback_to_course.author:
            author = obj.feedback_to_course.author.id
        else:
            author = None
        return {
            "id": obj.feedback_to_course.id if obj.feedback_to_course else None,
            "title": obj.feedback_to_course.name if obj.feedback_to_course else None,
            "author_id": author
        } if obj.feedback_to_course else None

    def get_replies(self, obj):
        return FeedbackBaseSerializer(obj.comments.all(), many=True, context=self.context).data

    def get_time_ago(self, obj):
        return FeedbackService.time_since_review(obj.feedback_date)


class CourseWithFeedbacksSerializer(serializers.ModelSerializer):
    feedbacks = FeedbackBaseSerializer(many=True, read_only=True)

    class Meta:
        model = Course
        fields = ['id', 'name', 'feedbacks']


class FeedbackCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feedback
        fields = ["id", "feedback_to_course", "feedback_text", "feedback_rating", "parent_feedback"]
        read_only_fields = ["feedback_date"]

    def validate(self, attrs):
        parent_feedback = attrs.get("parent_feedback")
        feedback_to_course = attrs.get("feedback_to_course")
        feedback_rating = attrs.get("feedback_rating")

        # If comment (have parent)
        if parent_feedback:
            if not parent_feedback.feedback_to_course:
                raise serializers.ValidationError(
                    {"parent_feedback": "Feedback should be attached to a course"}
                )

            attrs["feedback_to_course"] = parent_feedback.feedback_to_course  # take course from parent

            if feedback_rating is not None:
                raise serializers.ValidationError(
                    {"feedback_rating": "Comment cannot have rating values"}
                )

            if parent_feedback.parent_feedback:
                raise serializers.ValidationError(
                    {"parent_feedback": "Cannot add comment to comment"}
                )

        # If Feedback (not comment)
        else:
            if not feedback_to_course:
                raise serializers.ValidationError(
                    {"feedback_to_course": "Feedback should be attached to a course"}
                )
            if feedback_rating is None:
                raise serializers.ValidationError({"feedback_rating": "Feedback should have a rating"})

        return attrs

    def create(self, validated_data):
        validated_data["feedback_author"] = self.context["request"].user
        return super().create(validated_data)


class FeedbackUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feedback
        fields = ["feedback_text", "feedback_rating"]


class AuthorFeedbackTopSerializer(serializers.ModelSerializer):
    title = serializers.SerializerMethodField()
    total_rating = serializers.SerializerMethodField()
    total_feedbacks = serializers.SerializerMethodField()
    logo = serializers.SerializerMethodField()

    class Meta:
        model = Author
        fields = ('id', 'logo', 'title', 'full_title', 'legal_address',
                  'total_rating', 'total_feedbacks')

    def get_title(self, obj):
        return obj.title if obj.title else f'{obj.last_name} {obj.first_name} {obj.middle_name}'

    def get_logo(self, obj):
        if hasattr(obj, 'logo') and obj.logo:
            if hasattr(obj.logo, 'url'):
                return f'{settings.HOST_URL}{obj.logo.url}'
        if hasattr(obj, 'photo') and obj.photo:
            if hasattr(obj.photo, 'url'):
                return f'{settings.HOST_URL}{obj.photo.url}'
        return None

    def get_total_rating(self, instance) -> float:
        return instance.total_rating

    def get_total_feedbacks(self, instance) -> int:
        return instance.total_feedbacks


class FilterItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = ThematicsType
        fields = ('id', 'name', 'translations')


class AuthorFiltersSerializer(serializers.Serializer):
    courses_thematics = FilterItemSerializer(many=True)
    course_formats = FilterItemSerializer(many=True)
    course_levels = FilterItemSerializer(many=True)
    course_targets = FilterItemSerializer(many=True)
    learning_types = FilterItemSerializer(many=True)
    age_category = FilterItemSerializer(many=True)
    author_types = serializers.ListField(child=serializers.DictField())
