from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.tokens import default_token_generator
from django.db import transaction
from django.utils.http import urlsafe_base64_decode
from rest_framework.exceptions import ValidationError
from rest_framework import serializers
from djoser.serializers import (UserCreateSerializer
                                as DjoserUserCreateSerializer,
                                UserCreatePasswordRetypeSerializer)

from author.models import Author
from .validators import validate_bank_account, validate_payment_card
from student.models import Student
from django.conf import settings
User = get_user_model()


class UserValidationMixin:

    @staticmethod
    def validate_user_is_authenticated(user: User) -> None:

        if not user.is_authenticated:
            raise serializers.ValidationError({"Auth": "Please provide user credentials"})

    @staticmethod
    def validate_user_auth(auth_user: User, uid_user: User | None = None) -> None:
        if uid_user and auth_user != uid_user:
            raise serializers.ValidationError({"Auth": "Token and email are attached to different users."})
        if not auth_user.is_active:
            raise serializers.ValidationError({"Auth": "Your account has been disabled"})
        if not auth_user.email_is_verified:
            raise serializers.ValidationError({"Auth": "Your email has not been verified"})


class DeleteProfileSerializer(serializers.Serializer):
    reason = serializers.CharField(required=True)
    delete_checkbox = serializers.BooleanField(required=True)
    password = serializers.CharField(write_only=True)

    def validate_delete_checkbox(self, value):
        if not value:
            raise serializers.ValidationError("You must confirm the deletion.")
        return value


class BaseConfirmSerializer(serializers.Serializer, UserValidationMixin):
    uid = serializers.CharField()
    token = serializers.CharField()

    @staticmethod
    def decode_user_id_and_check_token(auth_user: User, uid: str, user_token: str) -> User:
        try:
            user = User.objects.get(pk=urlsafe_base64_decode(uid).decode())
        except Exception as e:
            raise ValidationError({"uid": f"{str(e)}"}, code=400)

        if not default_token_generator.check_token(user, user_token) or user != auth_user:
            raise ValidationError({"token": "Invalid token"})

        return user

    def validate(self, data):
        """
        Default validation for token validation.
        """
        uid = data.get("uid")
        token = data.get("token")
        auth_user = self.context["request"].user

        self.validate_user_is_authenticated(auth_user)
        uid_user = self.decode_user_id_and_check_token(auth_user, uid, token)
        self.validate_user_auth(auth_user, uid_user)

        return data


class ChangeEmailSerializer(serializers.Serializer, UserValidationMixin):
    """Serializer for email change validation."""
    password = serializers.CharField(write_only=True, required=True)
    new_email = serializers.EmailField()

    def validate(self, data):
        user_auth = self.context["request"].user
        self.validate_user_is_authenticated(user_auth)
        self.validate_user_auth(user_auth)
        password = data.get("password")
        if not user_auth.check_password(password):
            raise serializers.ValidationError({"password": "Wrong password"})
        new_email = data.get("new_email")
        if not User.objects.filter(email=new_email).exists():  # If email free
            if user_auth.email == new_email:
                raise serializers.ValidationError({"new_email": "Should be different from current"})
            return data
        raise serializers.ValidationError({"email": "User not found"})


class ChangePasswordSerializer(serializers.Serializer, UserValidationMixin):
    """Serializer for password change."""
    password = serializers.CharField(write_only=True, required=True)
    new_password = serializers.CharField(write_only=True, required=True)
    re_new_password = serializers.CharField(write_only=True, required=True)

    def validate(self, data):
        """Validate all fields"""
        user_auth = self.context["request"].user
        self.validate_user_is_authenticated(user_auth)
        password = data.get("password")
        self.validate_user_auth(user_auth)
        if not user_auth.check_password(password):
            raise serializers.ValidationError({"password": "Wrong old password"})
        new_pass = data.get("new_password")
        re_new_pass = data.get("re_new_password")
        if new_pass != re_new_pass:
            raise serializers.ValidationError({"re_new_pass": "New passwords doesn't match"})
        try:
            validate_password(new_pass)
        except ValidationError as e:
            raise serializers.ValidationError({"new_password": list(e.messages)})
        if user_auth.check_password(new_pass):
            raise serializers.ValidationError({"Auth": "New password should be different then previous one"})
        return data


class ChangePasswordConfirmSerializer(BaseConfirmSerializer):
    """Serializer for confirming password change"""
    new_password = serializers.CharField(write_only=True, required=True)

    def validate(self, data):
        data = super().validate(data)
        new_password = data.get("new_password")
        auth_user = self.context["request"].user
        try:
            validate_password(new_password)
        except ValidationError as e:
            raise serializers.ValidationError({"new_pass": list(e.messages)})
        else:
            if auth_user.check_password(new_password):
                raise serializers.ValidationError({"Auth": "Password already changed"})
            return data


class ChangeEmailConfirmSerializer(BaseConfirmSerializer):
    """Serializer for change email confirmation"""
    new_email = serializers.EmailField()

    def validate(self, data):
        data = super().validate(data)
        if User.objects.filter(email=data.get("new_email")).exists():
            raise serializers.ValidationError({"new_email": "Email is taken"})
        return data


class UserSerializer(serializers.ModelSerializer):
    account_type = serializers.SerializerMethodField()
    photo = serializers.SerializerMethodField()

    def get_photo(self, obj):
        if hasattr(obj, 'photo') and obj.photo:
            if hasattr(obj.photo, 'url'):
                return f'{settings.HOST_URL}{obj.photo.url}'

    def get_account_type(self, obj):
        if hasattr(obj, 'student'):
            return 2
        elif hasattr(obj, 'author'):
            return 3
        else:
            return 1

    class Meta:
        model = User
        fields = ['id', 'email', 'first_name', 'last_name', 'middle_name',
                  "photo", 'bio', 'birth_date', 'region',
                  'phone_number', 'photo', 'is_active', 'account_type']
        ref_name = "CustomUser"


class UserMeSerializer(serializers.Serializer):
    def to_representation(self, obj):
        if hasattr(obj, 'student'):
            from student.serializers import StudentSerializer
            return StudentSerializer(obj.student).data
        elif hasattr(obj, 'author'):
            from author.serializers import AuthorSerializer
            return AuthorSerializer(obj.author).data
        elif hasattr(obj, 'organization'):
            from organizations.serializers import OrganizationSerializer
            return OrganizationSerializer(obj.organization).data
        else:
            return UserSerializer(obj).data


class UserCreateSerializer(serializers.ModelSerializer):
    role = serializers.IntegerField(write_only=True)

    re_password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ['role', 'email', 'password', 're_password']

    @transaction.atomic
    def create(self, validated_data):
        role = validated_data.pop('role')
        re_password = validated_data.pop('re_password')
        if role == 3:
            author = Author(email=validated_data.get('email'))
            author.set_password(validated_data.get('password'))
            author.save()
            return author
        if role == 2:
            student = Student(email=validated_data.get('email'))
            student.set_password(validated_data.get('password'))
            student.save()
            return student
        raise ValidationError("Account type must be 2 or 3")


class CustomUserCreateSerializer(UserMeSerializer, DjoserUserCreateSerializer):
    """Without re_password"""
    pass


class CustomUserCreatePasswordRetypeSerializer(UserMeSerializer, UserCreatePasswordRetypeSerializer):
    """With re_password"""
    pass


class PaymentMethodSerializer(serializers.Serializer):
    payment_method = serializers.CharField(required=True)
    
    def validate_payment_method(self, value):
        if "-" in value:
            validate_payment_card(value)
        elif value.isdigit():
            validate_bank_account(value)
        else:
            raise serializers.ValidationError("Некорректный формат платежных данных.")
        return value