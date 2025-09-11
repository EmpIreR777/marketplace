from django.contrib.admin import register
from django.db import models
from django.utils.translation import gettext as _
from unfold import admin
from unfold.contrib.filters.admin import RangeDateFilter
from unfold.contrib.forms.widgets import WysiwygWidget

from courses.models import (
    Course,
    CourseImage,
    AdditionalDocument,
    ShortDescription,
    School,
    DirectionsType,
    LearningType,
    ThematicsType,
    CourseFormat,
    CourseLevel,
    LearningReasons,
    AgeCategory,
    ErrorReport
)


##############################################################################################################
# Inlines
##############################################################################################################
class CourseImageInline(admin.TabularInline):
    model = CourseImage
    fields = ('id', 'image')
    extra = 1
    max_num = 5
    tab = True
    can_delete = True


class AdditionalDocumentInline(admin.TabularInline):
    model = AdditionalDocument
    fields = ('id', 'file')
    extra = 1
    max_num = 10
    tab = True
    can_delete = True


class ShortDescriptionInline(admin.TabularInline):
    model = ShortDescription
    extra = 1
    max_num = 1
    tab = True
    can_delete = True


##############################################################################################################
# Admin Models
##############################################################################################################
@register(ErrorReport)
class ErrorReportAdmin(admin.ModelAdmin):
    list_display = ("id", "course", "error_type", "is_read", "created_at")
    list_filter = ("is_read", "error_type", "created_at")
    search_fields = ("course__title", "error_message")
    ordering = ("-created_at",)
    
    
@register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'author', 'duration', 'date_start', 'date_end', 'is_moderated', 'is_active')
    list_editable = ('is_moderated', 'is_active')
    ordering = ('name',)

    search_fields = ('id', 'name')
    list_filter_submit = True
    list_filter = ('is_moderated', 'is_active', 'is_wow_effect', 'is_top_sale', 'has_mentor',
                   'has_job_help', 'has_job_guarantee', 'trial_version', 'provides_diploma',
                   ('date_start', RangeDateFilter), ('date_end', RangeDateFilter))

    filter_horizontal = ('learning_types', 'course_levels', 'course_formats', 'courses_thematics',
                         'learning_reasons', 'age_category')
    readonly_fields = ('id',)
    fieldsets = (
        (_('Информация'), {'fields': ('author', 'name', 'link', 'tag', 'description', 'is_webinar',
                                      'is_moderated', 'is_active')}),
        (_('Популярность'), {'fields': ('is_top_sale', 'is_wow_effect')}),
        (_('Особенности'), {'fields': ('has_mentor', 'has_job_help', 'has_job_guarantee', 'trial_version',
                                       'provides_diploma', 'diploma_content')}),
        (_('Расписание'), {'fields': ('duration', 'date_start', 'date_end', 'is_duration_approximately')}),
        (_('Стоимость и оплата'), {'fields': ('price', 'without_discount_price', 'price_all',
                                              'price_installment', 'time_installment', 'return_conditions')}),
        (_('Формат обучения'), {'fields': ('learning_types', 'learning_reasons', 'age_category',
                                           'course_levels', 'course_formats', 'courses_thematics')}),
    )

    autocomplete_fields = ('author',)
    inlines = (CourseImageInline, AdditionalDocumentInline, ShortDescriptionInline)
    formfield_overrides = {
        models.TextField: {'widget': WysiwygWidget},
    }

    def get_queryset(self, request):
        return super().get_queryset(request).filter(school__isnull=True)


@register(School)
class SchoolAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'author', 'duration', 'date_start', 'date_end', 'is_moderated', 'is_active')
    list_editable = ('is_moderated', 'is_active')
    ordering = ('name',)

    search_fields = ('id', 'name')
    list_filter_submit = True
    list_filter = ('is_moderated', 'is_active', 'is_wow_effect', 'is_top_sale', 'has_mentor', 'has_job_help',
                   'has_job_guarantee', 'trial_version',  'has_parent_control', 'has_free_lesson',
                   'has_group', 'has_record', 'has_curator', 'provides_diploma',
                   ('date_start', RangeDateFilter), ('date_end', RangeDateFilter))

    filter_horizontal = ('learning_types', 'course_levels', 'course_formats', 'courses_thematics',
                         'learning_reasons', 'age_category')
    readonly_fields = ('id',)
    fieldsets = (
        (_('Информация'), {'fields': ('author', 'name', 'link', 'tag', 'description', 'location',
                                      'grade_from', 'grade_to', 'is_webinar', 'is_demo', 'is_active')}),
        (_('Популярность'), {'fields': ('is_top_sale', 'is_wow_effect')}),
        (_('Особенности'), {'fields': ('has_mentor', 'has_job_help', 'has_job_guarantee', 'trial_version',
                                       'has_parent_control', 'has_free_lesson', 'has_group', 'has_record',
                                       'has_curator', 'provides_diploma', 'diploma_content')}),
        (_('Расписание'), {'fields': ('duration', 'time_lessons', 'date_start', 'date_end',
                                      'is_duration_approximately')}),
        (_('Стоимость и оплата'), {'fields': ('price', 'without_discount_price', 'price_all',
                                              'price_installment', 'time_installment', 'return_conditions')}),
        (_('Формат обучения'), {'fields': ('learning_types', 'learning_reasons', 'age_category',
                                           'course_levels', 'course_formats', 'courses_thematics')}),
    )

    autocomplete_fields = ('author',)
    inlines = (CourseImageInline, AdditionalDocumentInline, ShortDescriptionInline)


@register(DirectionsType, LearningType, CourseFormat, CourseLevel,
          LearningReasons, AgeCategory)
class AdditionalAdmin(admin.ModelAdmin):
    list_display = ('name', 'translations')
    ordering = ('name', 'translations')
    search_fields = ('name', 'translations')


@register(ThematicsType)
class ThematicsTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'translations', 'learning_type__translations')
    ordering = ('name', 'translations')
    search_fields = ('name', 'translations')
    list_filter = ('learning_type__translations',)
    autocomplete_fields = ('learning_type',)
