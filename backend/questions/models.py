from django.db import models
from django.utils.translation import gettext as _
from django.core.exceptions import ValidationError


class OpennessChoices(models.TextChoices):
    LOW = 'low', _('Низкая')
    MEDIUM = 'medium', _('Средняя')
    HIGH = 'high', _('Высокая')


class AnswerCategory(models.TextChoices):
    IT = 'IT', _('IT')
    CREATIVITY = 'CREATIVITY', _('Творчество')
    SOCIAL_SCIENCE = 'SOCIAL_SCIENCE', _('Cоц. Науки')
    ECONOMICS = 'ECONOMICS', _('Экономика')
    ANALYTICS = 'ANALYTICS', _('Аналитика')


class Question(models.Model):
    title = models.CharField(
        verbose_name=_('Название'),
        default=None,
        max_length=255,
        null=True,
        blank=True,
    )
    text = models.CharField(
        verbose_name=_('Текст'),
        max_length=255,
    )
    has_multiple_answers = models.BooleanField(
        verbose_name=_('Имеет несколько ответов?'),
        default=True,
    )

    class Meta:
        verbose_name = _('Вопрос')
        verbose_name_plural = _('Вопросы')

    def __str__(self):
        return self.text if self.text else f'Question({self.id})'


class Answer(models.Model):
    question = models.ForeignKey(
        verbose_name=_('Вопрос'),
        to=Question,
        on_delete=models.CASCADE,
        related_name='answers',
    )
    text = models.CharField(
        verbose_name=_('Текст'),
        max_length=255,
    )
    answer_category = models.CharField(
        verbose_name=_('Категория'),
        default=None,
        max_length=15,
        choices=AnswerCategory.choices,
        null=True,
        blank=True,
    )
    openness_priority = models.CharField(
        verbose_name=_('Приоритет открытости новому'),
        default=None,
        max_length=10,
        choices=OpennessChoices.choices,
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = _('Ответ')
        verbose_name_plural = _('Ответы')

    def __str__(self):
        return self.text if self.text else f'Answer({self.id})'

    def clean(self):
        if self.answer_category and self.openness_priority:
            raise ValidationError('Нельзя указывать и "Категория" и "Приоритет открытости новому".')
        elif not self.answer_category and not self.openness_priority:
            raise ValidationError('Нужно указать или "Категория" или "Приоритет открытости новому".')

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
