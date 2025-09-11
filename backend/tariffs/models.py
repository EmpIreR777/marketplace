from uuid import uuid4

from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.translation import gettext as _
from rest_framework.exceptions import ValidationError

from tariffs.validators import validate_expire_date

User = get_user_model()


class TariffFeature(models.Model):
    tariff = models.ForeignKey(
        verbose_name=_('Тариф'),
        to='Tariff',
        on_delete=models.CASCADE,
        related_name='features',
    )
    text = models.CharField(
        verbose_name=_('Текст'),
        max_length=255,
    )

    class Meta:
        verbose_name = _('Предложение Тарифа')
        verbose_name_plural = _('Предложения Тарифа')

    def __str__(self):
        return self.text if self.text else f'TariffFeature({self.id})'


class TariffDurationType(models.TextChoices):
    TIMELESSLY = 'TIMELESSLY', _('Без срочный')
    MONTHLY = 'MONTHLY', _('Месячный')
    YEARLY = 'YEARLY', _('Годовой')


class Tariff(models.Model):
    name = models.CharField(
        verbose_name=_('Название'),
        max_length=255,
    )
    price = models.FloatField(
        verbose_name=_('Цена'),
        validators=[MinValueValidator(0)],
    )
    discount = models.PositiveSmallIntegerField(
        verbose_name=_('Скидка'),
        default=0,
        validators=[MaxValueValidator(100)],
        help_text=_('Скидка должна быть в диапазоне от 0 до 100. Пример: 42'),
    )
    percentage = models.PositiveSmallIntegerField(
        verbose_name=_('Процент с продаж'),
        help_text=_('Процент должен быть в диапазоне от 0 до 100. Пример: 42'),
        default=0,
        validators=[MaxValueValidator(100)],
    )
    is_show = models.BooleanField(
        verbose_name=_('Показывать?'),
        default=True,
    )
    is_active = models.BooleanField(
        verbose_name=_('Активен?'),
        default=True,
    )
    duration = models.CharField(
        verbose_name=_('Длительность'),
        default=TariffDurationType.MONTHLY,
        choices=TariffDurationType.choices,
        max_length=10,
    )

    class Meta:
        verbose_name = _('Тариф')
        verbose_name_plural = _('Тарифы')

    def __str__(self):
        return self.name if self.name else f'Tariff({self.id})'

    @property
    def total_price(self) -> float:
        if self.price:
            return round(self.price * (1 - self.discount / 100), 2)
        return 0


class UserTariff(models.Model):
    id = models.UUIDField(
        default=uuid4,
        primary_key=True,
        editable=False,
    )
    tariff = models.ForeignKey(
        verbose_name=_('Тариф'),
        to=Tariff,
        on_delete=models.PROTECT,
    )
    user = models.OneToOneField(
        verbose_name=_('Пользователь'),
        to=User,
        on_delete=models.PROTECT,
    )
    expire = models.DateTimeField(
        verbose_name=_('Дата окончания'),
        null=True,
        blank=True,
        validators=[validate_expire_date],
    )
    is_paid = models.BooleanField(
        verbose_name=_('Оплачен?'),
        default=False,
    )
    is_timeless = models.BooleanField(
        verbose_name=_('Без срока окончания?'),
        default=False,
    )

    class Meta:
        verbose_name = _('Оплаченный Тариф')
        verbose_name_plural = _('Оплаченные Тарифы')

    def clean(self):
        if not self.expire and not self.is_timeless:
            raise ValidationError(_('Нужно указать или "Дату окончания" или "Без срока окончания".'))
        elif self.expire and self.is_timeless:
            raise ValidationError('Нельзя указать и "Дату окончания" и "Без срока окончания".')

    def __str__(self):
        if self.tariff and self.user:
            return f'Тариф {self.tariff} для {self.user}'
        else:
            return f'Tariff({self.id})'
