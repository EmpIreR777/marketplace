from django.db import models
from django.utils.translation import gettext_lazy as _


class NotificationTypes(models.TextChoices):
    """
    Class store types of incoming notifications to user
    """
    EXPECTED_PAYMENT = 'Payment is expected', _('Ожидается оплата')
    PAYMENT_SUCCESS = 'Payment successful', _('Оплата прошла успешно')
    PAYMENT_FAILED = 'Payment failed', _('Оплата не прошла')
    UPDATE_OF_TERMS = 'Update of the terms', _('Обновление условий')
    CONFIRM_PARTICIPATION = 'Confirmation of participation', _('Подтверждение участия')
    MEET_REMINDER = 'A reminder about meeting', _('Напоминание о встрече')
    SCHEDULE_CHANGE = 'Schedule change', _('Изменения расписания')
    REGISTRATION_SUCCESS = 'Successful registration', _('Успешная регистрация')
    REFUND_APPROVED = 'Refund approved', _('Возврат оформлен')


class Notification(models.Model):
    """
    Notification model for user
    """
    user = models.ForeignKey(
        verbose_name=_('Пользователь'),
        to='userauth.CustomUser',
        on_delete=models.CASCADE,
        related_name='notifications',
        null=True,
        blank=True,
    )
    title = models.CharField(
        verbose_name=_('Название'),
        max_length=255,
    )
    body = models.TextField(
        verbose_name=_('Текст'),
        null=True,
        blank=True,
    )
    html = models.TextField(
        verbose_name=_('HTML формат'),
        null=True,
        blank=True,
    )
    notification_type = models.CharField(
        verbose_name=_('Тип'),
        choices=NotificationTypes,
        max_length=255,
    )
    is_read = models.BooleanField(
        verbose_name=_('Прочитано?'),
        default=False,
    )
    created_at = models.DateTimeField(
        verbose_name=_('Дата создания'),
        auto_now_add=True,
    )

    class Meta:
        verbose_name = _('Уведомление')
        verbose_name_plural = _('Уведомления')
        ordering = ['-created_at']

    def __str__(self):
        return self.title if self.title else f'Notification({self.id})'
