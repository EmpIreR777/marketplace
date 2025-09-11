from django.conf import settings
from django.contrib.admin import register
from django.db.models import Value
from django.db.models.functions import Concat
from django.utils.translation import gettext as _
from unfold import admin
from unfold.contrib.filters.admin import RangeDateTimeFilter
from unfold.decorators import display

from student.models import StudentCoursePurchase, Student
from userauth.admin import PaymentInline


##############################################################################################################
# Inlines
##############################################################################################################
class BoughtCourseInline(admin.TabularInline):
    model = StudentCoursePurchase
    extra = 0
    fields = ('course', 'purchase_date')
    readonly_fields = ('course', 'purchase_date')
    tab = True

    def get_readonly_fields(self, request, obj=None):
        if request.user.is_superuser and settings.DEBUG:
            return ('purchase_date',)
        return self.readonly_fields


##############################################################################################################
# Admin Models
##############################################################################################################
@register(StudentCoursePurchase)
class StudentCoursePurchaseAdmin(admin.ModelAdmin):
    list_display = ('student', 'course', 'purchase_date')

    list_filter = (('purchase_date', RangeDateTimeFilter),)
    search_fields = ('student__email', 'course__name')

    readonly_fields = ('student', 'course', 'purchase_date')
    fields = ('student', 'course', 'purchase_date')

    autocomplete_fields = ('student', 'course',)

    def get_readonly_fields(self, request, obj=None):
        if request.user.is_superuser and settings.DEBUG:
            return ('purchase_date',)
        return self.readonly_fields


@register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('email', 'full_name', 'email_is_verified', 'is_active', 'last_login')
    list_editable = ('email_is_verified', 'is_active')
    ordering = ('email',)

    search_fields = ('email', 'first_name', 'last_name', 'middle_name')
    list_filter_submit = True
    list_filter = ('email_is_verified', 'is_active', ('last_login', RangeDateTimeFilter))

    readonly_fields = ('id', 'last_login', 'full_name')
    fieldsets = (
        (_('Статус'), {'fields': ('is_active', 'deactivation_reason', 'last_login')}),
        (_('Контакты'), {'fields': ('email', 'email_is_verified', 'phone_number', 'region')}),
        (_('Профиль'), {'fields': ('photo', 'first_name', 'last_name', 'middle_name', 'bio')}),
    )

    inlines = (BoughtCourseInline, PaymentInline)

    @display(
        description='ФИО',
        ordering=Concat('last_name', Value(' '), 'first_name', Value(' '), 'middle_name'),
        empty_value='-',
    )
    def full_name(self, obj):
        return f'{obj.last_name} {obj.first_name} {obj.middle_name}'
