from django.shortcuts import get_object_or_404
from rest_framework.exceptions import ValidationError
from .models import Student, StudentCoursePurchase


class StudentRepository:

    @staticmethod
    def get_student_by_user(user):
        return get_object_or_404(Student, user=user)

    @staticmethod
    def get_student_purchases(student, ordering='purchase_date'):
        purchases = StudentCoursePurchase.objects.filter(student=student)

        if ordering in ['-purchase_date', 'purchase_date']:
            return purchases.order_by(ordering)
        return purchases.order_by('course__price')

    @staticmethod
    def get_student_purchase(student, course_id):
        return get_object_or_404(StudentCoursePurchase,
                                 student=student,
                                 course__id=course_id)

    @staticmethod
    def process_payment(student, course, payment_status):
        if payment_status != "success":
            raise ValidationError({"error": "Payment failed. Course was not purchased."})

        if StudentCoursePurchase.objects.filter(student=student, course=course).exists():
            raise ValidationError({"error": "Course already purchased."})

        return StudentCoursePurchase.objects.create(student=student, course=course)

    @staticmethod
    def delete_student(student, reason):
        student.deletion_reason = reason
        student.is_deleted = True
        student.save()

        student.user.photo.delete()
        student.user.is_active = False
        student.user.is_staff = False
        student.user.is_superuser = False
        student.user.save()
