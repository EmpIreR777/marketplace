import logging
from datetime import timedelta

from django.utils.timezone import now
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from author.serializers import AuthorForCourseSerializer
from core.settings import HOST_URL
from .models import (AdditionalDocument, AgeCategory, Course,
                     CourseFormat, CourseImage, CourseLevel, ErrorReport,
                     LearningReasons, LearningType, ShortDescription, ThematicsType, School)
from payments.models import Payment, PaymentType

logger = logging.getLogger(__name__)


class CourseBaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = "__all__"


class CourseOutSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField()
    course_image = serializers.SerializerMethodField()
    comments_count = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = ['id', 'author', 'price', 'name',
                  'course_image', 'duration', 'short_descriptions', 'comments_count',
                  'is_active', 'is_moderated'
                  ]

    def get_comments_count(self, obj):
        return obj.feedbacks.filter(is_approved=True).count()  # Do we need exclude comments on feedbacks?

    def get_author(self, obj):
        return obj.author.title if obj.author else None

    def get_course_image(self, obj):
        first_image = obj.images.first()
        return f"{HOST_URL}{first_image.image.url}" if first_image else None


class CourseImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseImage
        fields = ['image']


class CourseAdditionalDocumentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdditionalDocument
        fields = ['file']


class ShortDescriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShortDescription
        fields = ['text']


class CourseCreateSerializer(serializers.ModelSerializer):
    short_descriptions = ShortDescriptionSerializer(many=True, required=False)

    learning_types = serializers.PrimaryKeyRelatedField(queryset=LearningType.objects.all(),
                                                        many=True,
                                                        required=True)
    course_levels = serializers.PrimaryKeyRelatedField(queryset=CourseLevel.objects.all(),
                                                       many=True,
                                                       required=False)
    course_formats = serializers.PrimaryKeyRelatedField(queryset=CourseFormat.objects.all(),
                                                        many=True,
                                                        required=True)
    courses_thematics = serializers.PrimaryKeyRelatedField(queryset=ThematicsType.objects.all(),
                                                           many=True,
                                                           required=False)
    learning_reasons = serializers.PrimaryKeyRelatedField(queryset=LearningReasons.objects.all(),
                                                          many=True,
                                                          required=False)
    age_category = serializers.PrimaryKeyRelatedField(queryset=AgeCategory.objects.all(),
                                                      many=True,
                                                      required=True)

    class Meta:
        model = Course
        fields = [
            'date_start',
            'date_end', 'author',
            'link', 'learning_types',
            'price', 'name',
            'description', 'tag',
            'course_levels', 'course_formats',
            'courses_thematics', 'learning_reasons',
            'trial_version', 'return_conditions',
            'age_category',
            'is_active', 'short_descriptions'
        ]

    def update(self, instance, validated_data):
        short_descriptions_data = validated_data.pop('short_descriptions', [])

        # TODO fix miderated after update course
        # is_active = validated_data.pop('is_active', instance.is_active)

        # if validated_data or short_descriptions_data:
        #     instance.is_active = False
        #     instance.is_moderated = False

        instance = super().update(instance, validated_data)

        if short_descriptions_data:
            instance.short_descriptions.all().delete()
            ShortDescription.objects.bulk_create([
                ShortDescription(course=instance, **desc) for desc in short_descriptions_data
            ])

        return instance

    def to_internal_value(self, data):
        if isinstance(data, list):
            return [int(i) for i in data]
        return super().to_internal_value(data)

    def create(self, validated_data):
        request = self.context['request']
        logger.warning("FILES:", request.FILES)
        logger.warning("DATA:", request.data)

        additional_materials = request.FILES.getlist('additional_materials')
        logger.warning("ADDITIONAL_MATERIALS:", additional_materials if additional_materials else "None")
        m2m_fields = [
            'learning_types', 'course_levels',
            'course_formats', 'courses_thematics',
            'learning_reasons', 'age_category',
        ]
        missing_fields = [field for field in m2m_fields if field not in validated_data]
        if missing_fields:
            raise ValidationError({field: "This field is required." for field in missing_fields})
        logger.warning("validated_data:", validated_data)
        course = super().create(validated_data)

        AdditionalDocument.objects.bulk_create(
            [AdditionalDocument(course=course, file=doc) for doc in additional_materials])
        ShortDescription.objects.bulk_create([ShortDescription(course=course, **desc) for desc in
                                              validated_data.get('short_descriptions', [])])

        return course

    def validate_images(self, value):
        if len(value) > 5:
            raise serializers.ValidationError("Можно загрузить не более 5 фото.")
        return value


class CourseListSerializer(serializers.ModelSerializer):
    course_image = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = [
            'id', 'name', 'price', 'course_image'
        ]

    def get_course_image(self, obj):
        first_image = obj.images.first()
        return f"{HOST_URL}{first_image.image.url}" if first_image else None


class CourseDetailSerializer(CourseOutSerializer):
    is_returned = serializers.SerializerMethodField(read_only=True)
    author = AuthorForCourseSerializer(read_only=True)
    is_my_course = serializers.SerializerMethodField(read_only=True)
    is_bought = serializers.SerializerMethodField(read_only=True)
    course_images = serializers.SerializerMethodField()
    course_image = serializers.SerializerMethodField()
    learning_types = serializers.SerializerMethodField()
    course_formats = serializers.SerializerMethodField()
    course_levels = serializers.SerializerMethodField()
    courses_thematics = serializers.SerializerMethodField()
    learning_reasons = serializers.SerializerMethodField()
    age_category = serializers.SerializerMethodField()
    feedbacks_count = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = [
            'id',
            'is_my_course',
            'is_bought',
            'date_start', 'date_end',
            'author', 'link',
            'learning_types', 'name',
            'description', "course_images",
            "course_image", 'tag',
            'course_levels', 'course_formats',
            'courses_thematics', 'learning_reasons',
            'trial_version', 'return_conditions',
            'additional_materials', 'age_category',
            'is_active', 'price', 'feedbacks_count',
            'is_returned'
        ]

    def get_is_returned(self, obj):
        request = self.context.get('request', None)

        if not request or not hasattr(request, 'user'):
            return False

        user = request.user

        if not user.is_authenticated or not self.get_is_bought(obj):
            return False

        student_purchase = Payment.objects.filter(
            user=user,
            item_id=obj.id,
            payment_type=PaymentType.COURSE_PURCHASE
        ).order_by('-created_at').first()

        if not student_purchase:
            return False

        refund_deadline = student_purchase.created_at + timedelta(days=5)
        return now() <= refund_deadline

    def get_is_bought(self, obj):
        return self.context.get('is_bought', False)

    def get_feedbacks_count(self, obj):
        return obj.feedbacks.filter(is_approved=True).count() if obj.feedbacks else 0

    def get_is_my_course(self, obj):
        context = self.context.get('request')
        return False if not context else context.user.id == obj.author.id

    def get_course_images(self, obj):
        return [f"{HOST_URL}{image.image.url}" for image in obj.images.all()]

    def get_course_image(self, obj):
        first_image = obj.images.first()
        return f"{HOST_URL}{first_image.image.url}" if first_image else None

    def get_related_objects(self, obj, attr_name):
        return [{'id': item.id, 'name': item.name,
                 'translations': item.translations if hasattr(item, 'translations') else ''} for item in
                getattr(obj, attr_name).all()]

    def get_learning_types(self, obj):
        return self.get_related_objects(obj, 'learning_types')

    def get_course_levels(self, obj):
        return self.get_related_objects(obj, 'course_levels')

    def get_course_formats(self, obj):
        return self.get_related_objects(obj, 'course_formats')

    def get_courses_thematics(self, obj):
        return self.get_related_objects(obj, 'courses_thematics')

    def get_learning_reasons(self, obj):
        return self.get_related_objects(obj, 'learning_reasons')

    def get_age_category(self, obj):
        return self.get_related_objects(obj, 'age_category')


class CourseSerializer(serializers.ModelSerializer):
    is_school = serializers.BooleanField(default=False)

    class Meta:
        model = Course
        fields = '__all__'

    def to_representation(self, instance):
        if hasattr(instance, 'school'):
            return SchoolSerializer(instance.school).data
        return super().to_representation(instance)


class SchoolSerializer(serializers.ModelSerializer):
    is_school = serializers.BooleanField(default=True)

    class Meta:
        model = School
        fields = '__all__'


class CourseErrorSerializer(serializers.ModelSerializer):
    class Meta:
        model = ErrorReport
        fields = '__all__'
        read_only_fields = ['id', 'is_read', 'course', 'student']

    def create(self, validated_data):
        student = self.context.get('student')
        return ErrorReport.objects.create(**validated_data, is_read=False, student=student)


class MainPageStatisticSerializer(serializers.Serializer):
    courses = serializers.IntegerField()
    students = serializers.IntegerField()
    authors = serializers.IntegerField()
    sales = serializers.IntegerField()
    vuz = serializers.IntegerField()
