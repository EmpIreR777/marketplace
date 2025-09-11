from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.utils import timezone

from django.utils.translation import gettext_lazy as _


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError(_('Email должен быть указан.'))
        email = self.normalize_email(email)

        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        return self.create_user(email, password, **extra_fields)


class DeleteAccountReason(models.TextChoices):
    FEW_COURSES = 'FEW_COURSES', _('Мало курсов')
    DONT_FIND_INTERESTING_COURSES = 'DONT_FIND_INTERESTING_COURSES', _('Не нашел интересный курс')
    DONT_FIND_EXACT_COURSE = 'DONT_FIND_EXACT_COURSE', _('Не нашел точный курс')
    HIGHER_PRICE = 'HIGHER_PRICE', _('Высокая цена')
    OTHER = 'OTHER', _('Другое')


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(
        verbose_name=_('Email'),
        max_length=255,
        unique=True,
    )
    email_is_verified = models.BooleanField(
        verbose_name=_('Email подтверждён?'),
        default=False,
    )
    photo = models.ImageField(
        verbose_name=_('Фото аккаунта'),
        upload_to='user_photos/',
        null=True,
        blank=True,
    )
    first_name = models.CharField(
        verbose_name=_('Имя'),
        max_length=255,
        null=True,
        blank=True,
    )
    last_name = models.CharField(
        verbose_name=_('Фамилия'),
        max_length=255,
        null=True,
        blank=True,
    )
    middle_name = models.CharField(
        verbose_name=_('Отчество'),
        max_length=255,
        null=True,
        blank=True,
    )
    bio = models.TextField(
        verbose_name=_('Биография'),
        null=True,
        blank=True,
    )
    birth_date = models.DateField(
        verbose_name=_('Дата рождения'),
        null=True,
        blank=True,
    )
    region = models.CharField(
        verbose_name=_('Область'),
        max_length=255,
        null=True,
        blank=True,
    )
    phone_number = models.CharField(
        verbose_name=_('Номер телефона'),
        max_length=255,
        null=True,
        blank=True,
    )
    deactivation_reason = models.CharField(
        verbose_name=_('Причина удаления аккаунта'),
        max_length=255,
        choices=DeleteAccountReason.choices,
        null=True,
        blank=True,
    )
    is_staff = models.BooleanField(
        verbose_name=_('Админ?'),
        default=False,
    )
    is_active = models.BooleanField(
        verbose_name=_('Активный?'),
        default=False
    )
    payment_method = models.CharField(
        verbose_name=_('Метод оплаты'),
        max_length=50,
        blank=True,
        null=True,
    )
    created_at = models.DateTimeField(
        verbose_name=_('Дата создания'),
        auto_now_add=True
    )
    updated_at = models.DateTimeField(
        verbose_name=_('Дата обновления'),
        auto_now=True
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = CustomUserManager()

    class Meta:
        verbose_name = _('Пользователь')
        verbose_name_plural = _('Пользователи')

    def deactivate(self, reason):
        self.is_active = False
        self.deactivation_reason = reason
        self.save()

    def __str__(self):
        return self.email if self.email else f'User({self.id})'
