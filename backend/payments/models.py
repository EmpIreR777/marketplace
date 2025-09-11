from decimal import Decimal

from django.db import models
from django.utils.translation import gettext_lazy as _


class PaymentStatus(models.TextChoices):
    PROCESSING = 'processing', _('Обрабатывается')
    COMPLETED = 'completed', _('Выполнен')
    FAILED = 'failed', _('Провален')
    PAID = 'paid', _('Оплачен')


class PaymentType(models.TextChoices):
    SUBSCRIPTION = 'subscription', _('Подписка')
    COURSE_PURCHASE = 'course_purchase', _('Покупка Курса')
    REFUND = 'refund', _('Возврат')
    OTHER = 'other', _('Другое')


class Payment(models.Model):
    user = models.ForeignKey(
        verbose_name=_('Пользователь'),
        to='userauth.CustomUser',
        on_delete=models.CASCADE,
        related_name='payments'
    )
    item_id = models.CharField(
        verbose_name=_('ID предмета'),
        max_length=255,
        null=True,
        blank=True,
    )
    status = models.CharField(
        verbose_name=_('Статус'),
        max_length=255,
        choices=PaymentStatus.choices,
        default=PaymentStatus.PROCESSING
    )
    payment_type = models.CharField(
        verbose_name=_('Тип оплаты'),
        max_length=255,
        choices=PaymentType.choices,
        default=PaymentType.OTHER
    )
    amount = models.DecimalField(
        verbose_name=_('Сумма'),
        max_digits=10,
        decimal_places=2,
        default=Decimal('0.00'),
    )
    updated_at = models.DateTimeField(
        verbose_name=_('Дата Обновление'),
        auto_now=True
    )
    created_at = models.DateTimeField(
        verbose_name=_('Дата создания'),
        auto_now_add=True,
        db_index=True
    )
    yokassa_payment_id = models.CharField(
        max_length=255,
        verbose_name=_('ID платежа Yokassa'), 
        null=True, 
        blank=True)
    
    refund_reason = models.TextField(null=True, blank=True)

    class Meta:
        verbose_name = _('Платёж')
        verbose_name_plural = _('Платежи')

    def __str__(self):
        return f'Платёж от {self.user.email} #{self.item_id}'
