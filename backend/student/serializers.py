from rest_framework import serializers

from courses.serializers import CourseOutSerializer
from userauth.models import CustomUser
from student.models import Student, StudentCoursePurchase
from userauth.serializers import UserSerializer


class StudentDataSerializer(serializers.ModelSerializer):
    photo = serializers.ImageField(required=False)
    email = serializers.EmailField(required=False)

    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'first_name', 'last_name', 'middle_name',
                  'bio', 'birth_date', 'phone_number', 'photo']
        read_only_fields = ['id']


class StudentSerializer(UserSerializer):
    class Meta:
        model = Student
        fields = UserSerializer.Meta.fields


class StudentUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = [
            'id', 'photo', 'first_name', 'last_name', 'middle_name',
            'bio', 'birth_date', 'region', 'phone_number'
        ]

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance


class StudentOrderCoursesSerializer(serializers.ModelSerializer):
    course = CourseOutSerializer(read_only=True)

    class Meta:
        model = StudentCoursePurchase
        fields = ['id', 'course', 'purchase_date']
        

class DeleteStudentSerializer(serializers.Serializer):
    reason = serializers.CharField(required=True)
    delete_checkbox = serializers.BooleanField(required=True)
    password = serializers.CharField(write_only=True)

    def validate_delete_checkbox(self, value):
        if not value:
            raise serializers.ValidationError("You must confirm the deletion.")
        return value


class StudentScheduleSerializer(serializers.ModelSerializer):
    course_id = serializers.UUIDField(source='course.id', read_only=True)
    name = serializers.CharField(source='course.name', read_only=True)
    date_start = serializers.DateField(source='course.date_start', read_only=True)
    date_end = serializers.DateField(source='course.date_end', read_only=True)

    class Meta:
        model = StudentCoursePurchase
        fields = ('course_id', 'name', 'date_start', 'date_end')


class PaymentSerializer(serializers.Serializer):
    course_id = serializers.UUIDField(required=True)
    payment_status = serializers.CharField(required=True)
