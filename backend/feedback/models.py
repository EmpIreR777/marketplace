from django.db import models
from django.utils.translation import gettext as _


class Feedback(models.Model):
    feedback_author = models.ForeignKey(
        verbose_name=_('Автор'),
        to='userauth.CustomUser',
        on_delete=models.CASCADE,
        related_name='feedbacks',
    )
    feedback_to_course = models.ForeignKey(
        verbose_name='Курс',
        to='courses.Course',
        on_delete=models.CASCADE,
        related_name='feedbacks',
        null=True,
        blank=True,
    )
    feedback_date = models.DateTimeField(
        verbose_name=_('Дата создания'),
        auto_now_add=True,
    )
    feedback_text = models.TextField(
        verbose_name=_('Текст'),
        max_length=500,
    )
    feedback_rating = models.PositiveIntegerField(
        verbose_name=_('Рейтинг'),
        choices=[(i, i) for i in range(1, 6)],
        null=True,
        blank=True,
    )
    is_approved = models.BooleanField(
        verbose_name=_('Одобрен'),
        default=False,
    )
    parent_feedback = models.ForeignKey(
        verbose_name=_('Корневой отзыв'),
        to='self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='comments'
    )

    class Meta:
        verbose_name = _('Отзыв')
        verbose_name_plural = _('Отзывы')
        ordering = ['-feedback_date']
        indexes = [
            models.Index(fields=['feedback_rating']),
            models.Index(fields=['is_approved']),
            models.Index(fields=['feedback_date']),
        ]

    def __str__(self):
        if self.feedback_author and self.feedback_to_course:
            return f'{self.feedback_author}::{self.feedback_to_course}'
        else:
            return f'Feedback({self.id})'
