from django.db import models
from django.utils.translation import gettext_lazy as _

from author.models import Author


class Organization(Author):
    type = models.CharField(
        verbose_name=_('Тип'),
        max_length=255,
        null=True,
        blank=True,
    )
    partner_card = models.BooleanField(
        verbose_name=_('Есть карта партнёра?'),
        default=False,
    )
    license = models.CharField(
        verbose_name=_('Лицензия'),
        max_length=500,
        null=True,
        blank=True,
    )
    personal_account_name = models.CharField(
        verbose_name=_('Имя персонального аккаунта'),
        max_length=1000,
        null=True,
        blank=True,
    )
    personal_account_site = models.CharField(
        verbose_name=_('Сайт персонального аккаунта'),
        max_length=2000,
        blank=True,
        null=True,
    )
    leadership = models.CharField(
        verbose_name=_('Директор'),
        max_length=1000,
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = _('Организация')
        verbose_name_plural = _('Организации')

    def __str__(self):
        return self.title if self.title else f'Organization({self.id})'


class OrganizationRequisites(models.Model):
    organization = models.OneToOneField(
        verbose_name=_('Организация'),
        to=Organization,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    bik = models.CharField(
        verbose_name=_('БИК'),
        help_text=_('Банковский Идентификационный Код'),
        max_length=255,
        null=True,
        blank=True,
    )
    inn = models.CharField(
        verbose_name=_('ИНН'),
        help_text=_('Идентификационный Номер Налогоплательщика'),
        max_length=255,
        null=True,
        blank=True,
    )
    kpp = models.CharField(
        verbose_name=_('КПП'),
        help_text=_('Код Причины Постановки на учет'),
        max_length=255,
        null=True,
        blank=True,
    )
    ogrn = models.CharField(
        verbose_name=_('ОГРН'),
        help_text=_('Основной Государственный Регистрационный Номер'),
        max_length=255,
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = _('Реквизиты')
        verbose_name_plural = _('Реквизиты')

    def __str__(self):
        return f'Реквизиты организации {self.organization}'
