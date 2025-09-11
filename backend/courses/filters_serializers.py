from rest_framework import serializers
from author.models import Author
from courses.models import (
    AgeCategory, LearningType, ThematicsType,
    CourseFormat, CourseLevel, LearningReasons)


class PriceRangeSerializer(serializers.Serializer):
    price_min = serializers.IntegerField()
    price_max = serializers.IntegerField()


class LearningTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = LearningType
        fields = ["id", "name", "translations"]


class ThematicsTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ThematicsType
        fields = ["id", "name", "translations"]


class CourseFormatSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseFormat
        fields = ["id", "name", "translations"]


class CourseLevelSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseLevel
        fields = ["id", "name", "translations"]


class LearningReasonsSerializer(serializers.ModelSerializer):
    class Meta:
        model = LearningReasons
        fields = ["id", "name", "translations"]


class AgeCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = AgeCategory
        fields = ["id", "name", "translations"]


class AuthorTypeSerializer(serializers.Serializer):
    name = serializers.CharField()
    translations = serializers.CharField()


class CourseTypesSerializer(serializers.Serializer):
    courses_thematics = ThematicsTypeSerializer(many=True)
    course_formats = CourseFormatSerializer(many=True)
    course_levels = CourseLevelSerializer(many=True)
    course_targets = LearningReasonsSerializer(many=True)
    learning_types = LearningTypeSerializer(many=True)
    price = PriceRangeSerializer()
    age_category = AgeCategorySerializer(many=True)
    author_types = AuthorTypeSerializer(many=True)
