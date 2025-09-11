from django.db import models
from django.utils.translation import gettext as _


class Contact(models.Model):
    name = models.CharField(
        verbose_name=_('ФИО'),
        max_length=100,
    )
    email = models.EmailField()
    theme = models.CharField(
        verbose_name=_('Тема'),
        max_length=100
    )
    message = models.TextField(
        verbose_name=_('Сообщение')
    )
    is_agreed = models.BooleanField(
        verbose_name=_('Согласен?'),
        default=False,
    )
    created_at = models.DateTimeField(
        verbose_name=_('Дата создания'),
        auto_now_add=True,
    )
    is_read = models.BooleanField(
        verbose_name=_('Прочитано?'),
        default=False,
    )

    class Meta:
        db_table = 'contacts'
        verbose_name = _('Обращения')
        verbose_name_plural = _('Обращения')
        ordering = ['-created_at']

    def __str__(self):
        return self.name if self.name else f'Contact({self.name})'
