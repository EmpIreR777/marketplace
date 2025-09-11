from django.db.models.aggregates import Avg
from django.http import QueryDict
from django.db.models import Count, Q

from courses.filter import CourseFilter
from courses.models import Course


def parse_query_dict(query_dict: QueryDict) -> dict:
    parsed_query_dict = {}
    for query_field in query_dict:
        value = query_dict.getlist(query_field)
        if query_field == 'images[]':
            continue
        if '[]' in query_field:
            parsed_query_dict[query_field[:-2]] = value
        elif len(value) == 1:
            parsed_query_dict[query_field] = value[0]
    return parsed_query_dict


class AuthorService:
    @staticmethod
    def get_author_or_organization_or_none(user):
        if not user:
            return None
        if hasattr(user, 'author'):
            if hasattr(user.author, 'organization'):
                return user.author.organization
            return user.author
        return None


def get_top_courses(request, limit: int = 3):
    course_filter = CourseFilter(request.GET, queryset=Course.objects.all())
    return course_filter.qs.annotate(
        avg_rating=Avg(
            'feedbacks__feedback_rating',
            filter=Q(feedbacks__is_approved=True)
        )
    ).order_by('-avg_rating')[:limit]

def get_similar_courses(course, limit: int = 3):
    """
    Search for simular courses, by default limit is 3
    """
    similar_courses = Course.objects.filter(
        is_active=True
    ).exclude(id=course.id)

    similar_courses = similar_courses.annotate(
        thematic_match=Count('courses_thematics',
                             filter=Q(courses_thematics__in=course.courses_thematics.all())),
        format_match=Count('course_formats', filter=Q(course_formats__in=course.course_formats.all())),
        age_match=Count('age_category', filter=Q(age_category__in=course.age_category.all())),
        level_match=Count('course_levels', filter=Q(course_levels__in=course.course_levels.all())),
        reason_match=Count('learning_reasons', filter=Q(learning_reasons__in=course.learning_reasons.all())),
    ).order_by(
        '-thematic_match', '-format_match', '-age_match', '-level_match', '-reason_match'
    )[:limit]

    return similar_courses
