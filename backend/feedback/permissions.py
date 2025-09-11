from rest_framework import permissions


class IsCourseOwnerOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True

        if not request.user.is_authenticated:
            return False

        if request.method == "POST":
            parent_feedback_id = request.data.get('parent_feedback')
            if parent_feedback_id:
                from .models import Feedback
                try:
                    parent_feedback = Feedback.objects.get(id=parent_feedback_id)
                    course = parent_feedback.feedback_to_course
                    return course.owner == request.user
                except Feedback.DoesNotExist:
                    return False

        return True

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.feedback_author == request.user or request.user.is_staff


class IsOwnerOrAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.feedback_author == request.user or request.user.is_staff