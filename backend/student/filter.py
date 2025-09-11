import django_filters
from courses.models import AgeCategory, Course, CourseFormat, CourseLevel, \
    LearningType, ThematicsType


class StudentCourseFilter(django_filters.FilterSet):
    learning_types = django_filters.ModelMultipleChoiceFilter(
        field_name="learning_types__name",
        queryset=LearningType.objects.all(),
        to_field_name='name',
        conjoined=True
    )
    course_levels = django_filters.ModelMultipleChoiceFilter(
        field_name="course_levels__name",
        queryset=CourseLevel.objects.all(),
        to_field_name='name',
        conjoined=True
    )
    course_formats = django_filters.ModelMultipleChoiceFilter(
        field_name="course_formats__name",
        queryset=CourseFormat.objects.all(),
        to_field_name='name',
        conjoined=True
    )
    courses_thematics = django_filters.ModelMultipleChoiceFilter(
        field_name="courses_thematics__name",
        queryset=ThematicsType.objects.all(),
        to_field_name='name',
        conjoined=True
    )
    age_category = django_filters.ModelMultipleChoiceFilter(
        field_name="age_category__name",
        queryset=AgeCategory.objects.all(),
        to_field_name='name',
        conjoined=True
    )
    price_min = django_filters.NumberFilter(field_name='price',
                                            lookup_expr='gte',
                                            label="От (руб)")
    price_max = django_filters.NumberFilter(field_name='price',
                                            lookup_expr='lte',
                                            label="До (руб)")

    has_job_help = django_filters.BooleanFilter(field_name="has_job_help")
    has_job_guarantee = django_filters.BooleanFilter(field_name="has_job_guarantee")
    provides_diploma = django_filters.BooleanFilter(field_name="provides_diploma")
    has_mentor = django_filters.BooleanFilter(field_name="has_mentor")
    is_webinar = django_filters.BooleanFilter(field_name="is_webinar")
    is_top_sale = django_filters.BooleanFilter(field_name="is_top_sale")

    class Meta:
        model = Course
        fields = ['learning_types', 'course_levels', 'course_formats', 
                  'courses_thematics', 'age_category', 'has_job_help', 
                  'has_job_guarantee', 'provides_diploma', 'has_mentor', 
                  'is_webinar', 'is_top_sale', 'price_min', 'price_max']
