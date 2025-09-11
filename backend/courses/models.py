from enum import Enum
import uuid
from django.core.validators import FileExtensionValidator

from django.db import models
from courses.utils import get_path_upload_course_files, get_path_upload_course_image
from django.utils.translation import gettext_lazy as _


class DirectionsType(models.Model):
    name = models.CharField(
        verbose_name=_('Название'),
        max_length=255,
        unique=True,
    )
    translations = models.CharField(
        verbose_name=_('Перевод'),
        max_length=255,
        null=True,
        blank=True, 
        default=''
    )

    class Meta:
        verbose_name = _('Направление')
        verbose_name_plural = _('Направления')

    def __str__(self):
        return self.name


class LearningType(models.Model):
    name = models.CharField(
        verbose_name=_('Название'),
        max_length=255,
        unique=True,
    )
    translations = models.CharField(
        verbose_name=_('Перевод'),
        max_length=255,
        null=True,
        blank=True, 
        default=''
    )

    class Meta:
        verbose_name = _('Тип Обучения')
        verbose_name_plural = _('Типы Обучения')

    def __str__(self):
        return self.name


class ThematicsType(models.Model):
    name = models.CharField(
        verbose_name=_('Название'),
        max_length=255,
        unique=True,
    )
    translations = models.CharField(
        verbose_name=_('Перевод'),
        max_length=255,
        null=True,
        blank=True, 
        default=''
    )
    learning_type = models.ForeignKey(
        verbose_name=_('Тип обучения'),
        to=LearningType,
        on_delete=models.CASCADE,
        related_name='thematics',
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = _('Тематика')
        verbose_name_plural = _('Тематики')

    def __str__(self):
        return self.name


class CourseFormat(models.Model):
    name = models.CharField(
        verbose_name=_('Название'),
        max_length=255,
        unique=True,
    )
    translations = models.CharField(
        verbose_name=_('Перевод'),
        max_length=255,
        null=True,
        blank=True, 
        default=''
    )

    class Meta:
        verbose_name = _('Формат')
        verbose_name_plural = _('Форматы')

    def __str__(self):
        return self.name


class CourseLevel(models.Model):
    name = models.CharField(
        verbose_name=_('Название'),
        max_length=255,
        unique=True,
    )
    translations = models.CharField(
        verbose_name=_('Перевод'),
        max_length=255,
        null=True,
        blank=True, 
        default=''
    )

    class Meta:
        verbose_name = _('Уровень')
        verbose_name_plural = _('Уровни')

    def __str__(self):
        return self.name


class LearningReasons(models.Model):
    name = models.CharField(
        verbose_name=_('Название'),
        max_length=255,
        unique=True,
    )
    translations = models.CharField(
        verbose_name=_('Перевод'),
        max_length=255,
        null=True,
        blank=True, 
        default=''
    )

    class Meta:
        verbose_name = _('Причина обучения')
        verbose_name_plural = _('Причины обучения')

    def __str__(self):
        return self.name


class AgeCategory(models.Model):
    name = models.CharField(
        verbose_name=_('Название'),
        max_length=255,
        unique=True,
    )
    translations = models.CharField(
    verbose_name=_('Перевод'),
    max_length=255,
    null=True,
    blank=True, 
    default=''
)

    class Meta:
        verbose_name = _('Возрастная категория')
        verbose_name_plural = _('Возрастные категории')

    def __str__(self):
        return self.name


class Course(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
    author = models.ForeignKey(
        verbose_name=_('Автор'),
        to='author.Author',
        on_delete=models.SET_NULL,
        related_name='courses',
        null=True,
        blank=True,
    )
    link = models.TextField(
        verbose_name=_('Ссылка на курс'),
        max_length=2000,
        null=True,
        blank=True,
    )
    name = models.CharField(
        verbose_name=_('Название'),
        max_length=1000,
    )
    description = models.TextField(
        verbose_name=_('Описание'),
        max_length=2000,
        null=True,
        blank=True,
    )
    tag = models.CharField(
        max_length=255,
        null=True, blank=True,
        verbose_name=_('Тэг')
    )
    duration = models.DurationField(
        verbose_name=_('Длительность курса'),
        null=True,
        blank=True,
    )
    is_duration_approximately = models.BooleanField(
        verbose_name=_("Длительность курса приблизительна?"),
        default=False,
    )
    date_start = models.DateField(
        verbose_name=_('Дата начала'),
        blank=True,
        null=True,
    )
    date_end = models.DateField(
        verbose_name=_('Дата конца'),
        null=True,
        blank=True,
    )
    portfolio_text = models.TextField(
        verbose_name=_('Портфолио'),
        max_length=2000,
        blank=True,
        null=True,
    )
    price = models.DecimalField(
        verbose_name=_('Цена'),
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
    )
    price_all = models.DecimalField(
        verbose_name=_('Общая цена'),
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
    )
    without_discount_price = models.DecimalField(
        verbose_name=_('Цена без скидки'),
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
    )
    price_installment = models.DecimalField(
        verbose_name=_('Цена в рассрочку'),
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
    )
    time_installment = models.IntegerField(
        verbose_name=_('Время рассрочки'),
        null=True,
        blank=True,
    )
    return_conditions = models.TextField(  # Нету в парсере
        verbose_name=_('Условия возврата'),
        max_length=2000,
        null=True,
        blank=True,
    )
    learning_types = models.ManyToManyField(
        verbose_name=_('Типы изучения'),
        to=LearningType,
        blank=True,
    )
    course_levels = models.ManyToManyField(
        verbose_name=_('Уровни'),
        to=CourseLevel,
        blank=True,
    )
    course_formats = models.ManyToManyField(
        verbose_name=_('Форматы'),
        to=CourseFormat,
        blank=True,
    )
    courses_thematics = models.ManyToManyField(
        verbose_name=_('Тематики'),
        to=ThematicsType,
        blank=True,
        related_name='courses'
    )
    learning_reasons = models.ManyToManyField(
        verbose_name=_('Причины изучения'),
        to=LearningReasons,
        blank=True,
    )
    age_category = models.ManyToManyField(
        AgeCategory,
        blank=True,
        verbose_name=_('Возрастные категории')
    )
    has_job_help = models.BooleanField(
        verbose_name=_('Есть помощь с поиском работы?'),
        default=False,
    )
    has_job_guarantee = models.BooleanField(
        verbose_name=_('Есть гарантия трудоустройства?'),
        default=False,
    )
    provides_diploma = models.BooleanField(
        verbose_name=_('Выдают диплом?'),
        default=False,
    )
    diploma_content = models.TextField(
        verbose_name=_('Информация об дипломе'),
        max_length=2000,
        null=True,
        blank=True,
    )
    has_mentor = models.BooleanField(
        verbose_name=_('Есть ментор?'),
        default=False,
    )
    is_webinar = models.BooleanField(
        verbose_name=_('Это вебинар?'),
        default=False,
    )
    is_top_sale = models.BooleanField(
        verbose_name=_('Топ продаж?'),
        default=False,
    )
    is_wow_effect = models.BooleanField(
        verbose_name=_('Вау эффект?'),
        default=False,
    )
    trial_version = models.BooleanField(  # Нету в парсере
        verbose_name=_('Есть пробная версия?'),
        default=False,
    )
    is_moderated = models.BooleanField(
        verbose_name=_('Курс одобрен?'),
        default=False,
    )
    is_active = models.BooleanField(
        verbose_name=_('Курс активен?'),
        default=True,
    )

    class Meta:
        verbose_name = _('Курс')
        verbose_name_plural = _('Курсы')

    def save(self, *args, **kwargs):
        if (self.author and
                self.author and
                self.author.is_active and
                self.author.email_is_verified):
            if self.author.is_verified and not self.pk:
                self.is_moderated = True
                self.is_active = True
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name if self.name else f'Course({self.id})'


class School(Course):
    location = models.JSONField(
        verbose_name=_('Локация'),
        null=True,
        blank=True,
    )
    time_lessons = models.DurationField(
        verbose_name=_('Длительность урока'),
        null=True,
        blank=True,
    )
    grade_from = models.PositiveSmallIntegerField(
        verbose_name=_('Мин. класс'),
        null=True,
        blank=True,
    )
    grade_to = models.PositiveSmallIntegerField(
        verbose_name=_('Макс. класс'),
        null=True,
        blank=True,
    )
    directions = models.ManyToManyField(
        verbose_name=_('Направления'),
        to=DirectionsType,
        related_name='directions',
        blank=True,
    )
    is_demo = models.BooleanField(
        verbose_name=_('Демо?'),
        default=False,
    )
    has_parent_control = models.BooleanField(
        verbose_name=_('Есть родительский контроль?'),
        default=False,
    )
    has_free_lesson = models.BooleanField(
        verbose_name=_('Есть бесплатные уроки?'),
        default=False,
    )
    has_group = models.BooleanField(
        verbose_name=_('Есть групповые занятия?'),
        default=False,
    )
    has_record = models.BooleanField(
        verbose_name=_('Есть запись уроков?'),
        default=False,
    )
    has_curator = models.BooleanField(
        verbose_name=_('Есть куратор?'),
        default=False,
    )

    class Meta:
        verbose_name = _('Школа')
        verbose_name_plural = _('Школы')

    def __str__(self):
        return self.name if self.name else f'School({self.id})'


class CourseImage(models.Model):
    course = models.ForeignKey(
        verbose_name=_('Курс'),
        to=Course,
        on_delete=models.CASCADE,
        related_name='images',
    )
    image = models.ImageField(
        verbose_name=_('Изображение'),
        upload_to=get_path_upload_course_image,
        validators=[
            FileExtensionValidator(
                allowed_extensions=['jpg', 'jpeg', 'png', 'webp'],
                message='Допустимые расширения: .jpg, .jpeg, .png, .webp'
            ),
        ],
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = _('Изображение Курса')
        verbose_name_plural = _('Изображения Курсов')

    def __str__(self):
        return f'Изображение к курсу {self.course}'


class AdditionalDocument(models.Model):
    course = models.ForeignKey(
        verbose_name=_('Курс'),
        to=Course,
        on_delete=models.CASCADE,
        related_name='additional_materials'
    )
    file = models.FileField(
        verbose_name=_('Файл'),
        upload_to=get_path_upload_course_files,
        validators=[
            FileExtensionValidator(
                allowed_extensions=['pdf', 'doc', 'docx', 'txt', 'jpg', 'jpeg', 'png'],
                message="Допустимые расширения: .pdf, .doc, .docx, .txt"
            ),
        ],
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = _('Доп. Документ')
        verbose_name_plural = _('Доп. Документы')

    def __str__(self):
        return f'Доп. документы к курсу {self.course}'


class ShortDescription(models.Model):
    course = models.ForeignKey(
        verbose_name=_('Курс'),
        to=Course,
        on_delete=models.CASCADE,
        related_name='short_descriptions',
    )
    text = models.CharField(
        verbose_name=_('Текст'),
        max_length=250,
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = _('Краткое Описание')
        verbose_name_plural = _('Краткие Описания')

    def __str__(self):
        return f'Краткое описание к курсу {self.course}'
    


class ErrorReportType(models.TextChoices):
    TECHNICAL_ISSUE = 'Technical Issue', _('Техническая ошибка')
    CONTENT_ERROR = 'Content Error', _('Ошибка в контенте')
    PAYMENT_ERROR = 'Payment Error', _('Ошибка в платёжной системе')
    OTHER = 'Other', _('Другая ошибка')
    

class ErrorReport(models.Model):
    course = models.ForeignKey(
        'Course',
        on_delete=models.CASCADE,
        related_name='error_reports',
        verbose_name=_('Курс')
    )
    student = models.ForeignKey(
        'student.Student',
        on_delete=models.CASCADE,
        related_name='error_reports',
        verbose_name=_('Студент')
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('Дата сообщения')
    )
    error_type = models.CharField(
        max_length=255,
        choices=ErrorReportType.choices,
        verbose_name=_('Тип ошибки')
    )
    error_message = models.TextField(
        verbose_name=_('Сообщение об ошибке')
    )
    is_read = models.BooleanField(
        default=False,
        verbose_name=_('Ошибка прочитана?')
    )

    class Meta:
        verbose_name = _('Сообщение об ошибке')
        verbose_name_plural = _('Сообщения об ошибках')
        ordering = ['-created_at']
        default_related_name = 'error_reports'
        db_table = 'error_reports'
        indexes = [
            models.Index(fields=['created_at']),
            models.Index(fields=['error_type']),
        ]
        

    def __str__(self):
        return f'Ошибка на курсе {self.course.name}'
    
