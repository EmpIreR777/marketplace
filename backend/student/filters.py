import django_filters
from datetime import timedelta
from django.utils.timezone import now
from rest_framework.exceptions import APIException

from student.models import StudentCoursePurchase


class StudentCourseScheduleFilter(django_filters.FilterSet):
    filter = django_filters.CharFilter(method='filter_by_period')

    class Meta:
        model = StudentCoursePurchase
        fields = []

    def filter_by_period(self, queryset, name, value):
        today = now().date()

        filter_options = {
            "week": (today - timedelta(days=today.weekday()),
                     today - timedelta(days=today.weekday()) + timedelta(days=6)),
            "month": (today.replace(day=1),
                      (today.replace(day=28) + timedelta(days=4)).replace(day=1) - timedelta(days=1)),
            "year": (today.replace(month=1, day=1), today.replace(month=12, day=31))
        }

        if value not in filter_options:
            raise APIException(f"Invalid filter parameter: {value}. Allowed: week, month, year")

        start_date, end_date = filter_options[value]

        return queryset.filter(
            course__date_start__lte=end_date,
            course__date_end__gte=start_date
        )
