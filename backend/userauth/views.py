from django.contrib.auth.tokens import default_token_generator
from django.core.exceptions import ValidationError
from django.http import JsonResponse
from django.utils.timezone import now
from django.middleware.csrf import get_token
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import get_user_model
from django.utils.encoding import force_bytes

from djoser.views import UserViewSet as DjoserUserViewSet
from djoser.conf import settings as djoser_settings
from djoser.compat import get_user_email
from djoser import signals

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.decorators import action
from rest_framework.exceptions import APIException
from rest_framework.mixins import CreateModelMixin
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken

from drf_yasg.utils import swagger_auto_schema

from author.models import Author
from student.models import Student
from .serializers import (
    ChangeEmailSerializer,
    ChangeEmailConfirmSerializer,
    ChangePasswordSerializer,
    ChangePasswordConfirmSerializer,
    PaymentMethodSerializer,
    UserMeSerializer, UserCreateSerializer
)
from .services.email_service import (
    UserChangeEmailNotificationMail,
    UserSuccessEmailChangeNotificationMail,
    UserChangePasswordNotificationMail,
    UserSuccessChangePasswordNotificationMail,
    UserChangeEmailOldNotification
)

User = get_user_model()


class UserViewSet(CreateModelMixin, GenericViewSet):
    queryset = DjoserUserViewSet.queryset
    http_method_names = ['get', 'post']
    token_generator = default_token_generator

    def get_serializer_class(self):
        if self.action == "create":
            return UserCreateSerializer
        elif self.action == "destroy" or (
                self.action == "me" and self.request and self.request.method == "DELETE"
        ):
            return djoser_settings.SERIALIZERS.user_delete
        elif self.action == "activation":
            return djoser_settings.SERIALIZERS.activation
        elif self.action == "resend_activation":
            return djoser_settings.SERIALIZERS.password_reset
        elif self.action == "reset_password":
            return djoser_settings.SERIALIZERS.password_reset
        elif self.action == "reset_password_confirm":
            return djoser_settings.SERIALIZERS.password_reset_confirm
        elif self.action == "set_password":
            return ChangePasswordSerializer
        elif self.action == "set_password_confirm":
            return ChangePasswordConfirmSerializer
        elif self.action == "set_email":
            return ChangeEmailSerializer
        elif self.action == "set_email_confirm":
            return ChangeEmailConfirmSerializer
        elif self.action == "reset_username":
            return djoser_settings.SERIALIZERS.username_reset
        elif self.action == "reset_username_confirm":
            if djoser_settings.USERNAME_RESET_CONFIRM_RETYPE:
                return djoser_settings.SERIALIZERS.username_reset_confirm_retype
            return djoser_settings.SERIALIZERS.username_reset_confirm
        elif self.action == "me":
            return UserMeSerializer
        return self.serializer_class

    def get_permissions(self):
        if self.action in ['set_password', 'set_password_confirm']:
            permission_classes = djoser_settings.PERMISSIONS.set_password
        elif self.action in ['set_username', 'set_username_confirm']:
            permission_classes = djoser_settings.PERMISSIONS.set_username
        elif self.action == "me" and self.request and self.request.method == "GET":
            permission_classes = djoser_settings.PERMISSIONS.user
        else:
            permission_classes = []

        if not isinstance(permission_classes, list):
            permission_classes = [permission_classes]

        return [permission() for permission in permission_classes]

    def perform_create(self, serializer, *args, **kwargs):
        print(serializer.validated_data)
        user = serializer.save(*args, **kwargs)
        signals.user_registered.send(
            sender=self.__class__, user=user, request=self.request
        )

        context = {"user": user}
        to = [get_user_email(user)]
        if djoser_settings.SEND_ACTIVATION_EMAIL:
            djoser_settings.EMAIL.activation(self.request, context).send(to)
        elif djoser_settings.SEND_CONFIRMATION_EMAIL:
            djoser_settings.EMAIL.confirmation(self.request, context).send(to)

    @action(detail=False, methods=['post'], )
    def activation(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        uid = request.data.get("uid")
        token = request.data.get("token")
        print(uid, token)
        try:
            uid = urlsafe_base64_decode(uid).decode()
            user = User.objects.get(pk=uid)
        except (User.DoesNotExist, ValueError, TypeError):
            raise APIException("User by uid and token not found")
        if default_token_generator.check_token(user, token):
            user.is_active = True
            user.email_is_verified = True
            user.save()
            
            if Author.objects.filter(pk=user.pk).exists():
                role = "Автор"
            elif Student.objects.filter(pk=user.pk).exists():
                role = "Студент"
            else:
                role = "Неизвестно"
            print(f'sending notification to: {settings.ADMINS.split(",")}')
            send_mail(
                subject=f"Зарегистрирован новый {role}",
                message=f"Новый пользователь {user.email} зарегистрирован как {role}.",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=settings.ADMINS.split(","),
                fail_silently=False,
            )
            
            refresh = RefreshToken.for_user(user)
            return Response({
                "message": "Activated successfully",
                "access_token": str(refresh.access_token),
                "refresh_token": str(refresh),
                "is_success": True
            }, status=status.HTTP_200_OK)
        raise APIException("User for this token not found")

    @action(["post"], detail=False)
    def resend_activation(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.get_user(is_active=False)

        if not djoser_settings.SEND_ACTIVATION_EMAIL:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        if user:
            context = {"user": user}
            to = [get_user_email(user)]
            djoser_settings.EMAIL.activation(self.request, context).send(to)

        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(["post"], detail=False, url_path=f"reset_{User.USERNAME_FIELD}")
    def reset_username(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.get_user()

        if user:
            context = {"user": user}
            to = [get_user_email(user)]
            djoser_settings.EMAIL.username_reset(self.request, context).send(to)

        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(["post"], detail=False, url_path=f"reset_{User.USERNAME_FIELD}_confirm")
    def reset_username_confirm(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        new_username = serializer.data["new_" + User.USERNAME_FIELD]

        setattr(serializer.user, User.USERNAME_FIELD, new_username)
        if hasattr(serializer.user, "last_login"):
            serializer.user.last_login = now()
        serializer.user.save()

        if djoser_settings.USERNAME_CHANGED_EMAIL_CONFIRMATION:
            context = {"user": serializer.user}
            to = [get_user_email(serializer.user)]
            djoser_settings.EMAIL.username_changed_confirmation(self.request, context).send(to)
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(["post"], detail=False)
    def reset_password(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.get_user()

        if user:
            context = {"user": user}
            to = [get_user_email(user)]
            djoser_settings.EMAIL.password_reset(self.request, context).send(to)

        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(["post"], detail=False)
    def reset_password_confirm(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        uid = request.data.get("uid")
        token = request.data.get("token")
        new_password = request.data.get("new_password")
        try:
            uid = urlsafe_base64_decode(uid).decode()
            user = User.objects.get(pk=uid)
        except (User.DoesNotExist, ValueError, TypeError):
            raise APIException("User by uid and token not found")
        if not default_token_generator.check_token(user, token):
            raise APIException("Invalid or expired token")
        try:
            validate_password(new_password, user)
        except ValidationError:
            raise APIException("Cannot validate new password")
        user.set_password(new_password)
        user.save()
        refresh = RefreshToken.for_user(user)
        return Response({
            "message": "Password reset successfully",
            "access_token": str(refresh.access_token),
            "refresh_token": str(refresh),
            "is_success": True
        }, status=status.HTTP_200_OK)

    @action(["post"], detail=False, url_path="set_password")
    def set_password(self, request, *args, **kwargs):

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = self.request.user
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)
        context = {
            "user": user,
            "uid": uid,
            "token": token,
            "is_success": True,
        }
        try:
            success_email = UserChangePasswordNotificationMail(self.request, context)
            success_email.send([user.email])
        except ValidationError:
            raise APIException("Failed to send confirmation email")
        return Response({"message": "Confirmation email sent to your current email address",
                         "is_success": True},
                        status=status.HTTP_202_ACCEPTED)

    @action(["post"], detail=False, url_path="set_password_confirm")
    def set_password_confirm(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        new_password = serializer.validated_data["new_password"]
        auth_user = self.request.user
        try:
            uid = urlsafe_base64_decode(serializer.validated_data["uid"]).decode()
            user = User.objects.get(pk=uid)
            token = default_token_generator.make_token(user)
        except (User.DoesNotExist, ValueError, TypeError):
            raise APIException("User by uid and token not found")
        if user != auth_user:
            raise APIException("Token user and user do not match")
        if not default_token_generator.check_token(user, serializer.validated_data["token"]):
            raise APIException("User by uid and token not found")
        try:
            auth_user.set_password(new_password)
            context = {
                "user": user,
                "uid": uid,
                "token": token,
            }
            UserSuccessChangePasswordNotificationMail(self.request, context).send([auth_user.email])
        except Exception:
            raise APIException("Failed to send confirmation email")
        auth_user.save()
        return Response(
            {"message": "Password changed successfully", "is_success": True},
            status=status.HTTP_200_OK
        )

    @action(["post"], detail=False, url_path=f"set_{User.USERNAME_FIELD}")
    def set_email(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = self.request.user
        new_email = serializer.validated_data["new_email"]

        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)

        context = {
            "user": user,
            "new_email": new_email,
            "uid": uid,
            "token": token,
            "is_success": True
        }
        try:
            notify_email = UserChangeEmailOldNotification(self.request, {"new_email": new_email})
            notify_email.send([user.email])
            success_email = UserChangeEmailNotificationMail(self.request, context)
            success_email.send([new_email])
        except ValidationError:
            raise APIException("Failed to send confirmation email")
        return Response({
            "message": "Confirmation email sent to your current email address",
            "is_success": True
        }, status=status.HTTP_202_ACCEPTED)

    @action(["post"], detail=False, url_path="set_email_confirm")
    def set_email_confirm(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        new_email = serializer.validated_data["new_email"]
        try:
            uid = urlsafe_base64_decode(serializer.validated_data["uid"]).decode()
            user = User.objects.get(pk=uid)
        except (User.DoesNotExist, ValueError, TypeError):
            raise APIException("User by uid and token not found")
        if User.objects.filter(email=new_email).exists():
            raise APIException("Email is already taken")
        token = serializer.validated_data["token"]
        if not default_token_generator.check_token(user, token):
            raise APIException("Invalid or expired token")
        try:
            user.email = new_email
            context = {
                "user": user,
                "new_email": new_email
            }
            UserSuccessEmailChangeNotificationMail(self.request, context).send([new_email])
        except Exception:
            raise APIException("Failed to complete password change")
        user.save()
        return Response(
            {"message": "Email changed successfully", "is_success": True},
            status=status.HTTP_200_OK
        )

    def destroy(self, request, *args, **kwargs):
        user = self.get_object()
        user.is_active = False
        user.save()
        return Response(status=status.HTTP_204_NO_CONTENT, data={"is_success": True})

    @action(detail=False, methods=['get'], url_path='me')
    def me(self, request, *args, **kwargs):
        return Response(self.get_serializer(request.user).data)


def get_csrf_token(request):
    return JsonResponse({'csrfToken': get_token(request)})


class PaymentMethodView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(request_body=PaymentMethodSerializer)
    def post(self, request):
        serializer = PaymentMethodSerializer(data=request.data)
        if serializer.is_valid():
            request.user.payment_method = serializer.validated_data["payment_method"]
            request.user.save()
            return Response({"message": "Платежные данные обновлены."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    