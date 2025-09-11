from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext as _


User = get_user_model()


class StudentCoursePurchase(models.Model):
    student = models.ForeignKey(
        verbose_name=_('Студент'),
        to='Student',
        on_delete=models.CASCADE,
        related_name='orders',
    )
    course = models.ForeignKey(
        verbose_name=_('Курс'),
        to='courses.Course',
        on_delete=models.CASCADE,
        related_name='purchases',
    )
    purchase_date = models.DateTimeField(
        verbose_name=_('Дата покупки'),
        auto_now_add=True,
    )

    class Meta:
        verbose_name = _('Приобретённый курс')
        verbose_name_plural = _('Приобретённые курсы')
        unique_together = ('student', 'course')


class Student(User):
    bought_courses = models.ManyToManyField(
        verbose_name=_('Купленные курсы'),
        to='courses.Course',
        through=StudentCoursePurchase,
        related_name='buyers'
    )

    class Meta:
        verbose_name = _('Студент')
        verbose_name_plural = _('Студенты')

    def __str__(self):
        return self.email if self.email else f'Student({self.id})'
