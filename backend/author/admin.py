from django.contrib.admin import register
from django.db import models
from django.db.models import Value
from django.db.models.functions import Concat
from django.utils.translation import gettext as _
from unfold import admin
from unfold.contrib.filters.admin import RangeDateTimeFilter
from unfold.decorators import display
from unfold.contrib.forms.widgets import WysiwygWidget
from django.urls import reverse
from django.utils.html import format_html

from author.models import Author, AuthorType, DocumentType, Document, FIZAuthor, FOPAuthor, LLCAuthor, RequiredDocument
from courses.models import Course, School
from userauth.admin import PaymentInline


##############################################################################################################
# Inlines
##############################################################################################################
class DocumentInline(admin.TabularInline):
    model = Document
    fields = ('id', 'author', 'document_type', 'file')
    readonly_fields = ('id',)
    extra = 1
    tab = True
    show_change_link = True
    can_delete = True


class CourseInline(admin.StackedInline):
    model = Course
    fields = ('id', 'name')
    readonly_fields = ('id',)
    extra = 0
    tab = True
    show_change_link = True
    can_delete = True

    def get_queryset(self, request):
        return super().get_queryset(request).filter(school__isnull=True)


class SchoolInline(admin.StackedInline):
    model = School
    fields = ('id', 'name')
    readonly_fields = ('id',)
    extra = 0
    tab = True
    show_change_link = True
    can_delete = True
    
##############################################################################################################
# Verification Inlines
##############################################################################################################
class FizAuthorInline(admin.StackedInline):
    model = FIZAuthor
    verbose_name = _('Верификационные данные')
    fields = ('fio', 'fio_short', 'passport_serial', 'passport_number', 'passport_date', 'passport_issued_by',
              'passport_code_department', 'inn', 'contact_number', 'address', 'snils', 'bank_name',
              'bank_bik', 'bank_ks', 'bank_rs', 'email')
    readonly_fields = ('fio', 'fio_short', 'passport_serial', 'passport_number', 'passport_date', 
                       'passport_issued_by',
                       'passport_code_department', 'inn', 'contact_number', 'address', 'snils', 'bank_name',
                       'bank_bik', 'bank_ks', 'bank_rs', 'email')
    extra = 0
    tab = True
    show_change_link = False
    can_delete = False


class FOPAuthorInline(admin.StackedInline):
    model = FOPAuthor
    verbose_name = _('Верификационные данные')
    fields = ('fio', 'fio_short', 'reg_number', 'reg_date', 'address',
              'contact_number', 'inn', 'bank_name', 'bank_bik',
              'bank_ks', 'bank_rs', 'ogrnip_number', 'email')
    readonly_fields = ('fio', 'fio_short', 'reg_number', 'reg_date', 'address',
                       'contact_number', 'inn', 'bank_name', 'bank_bik',
                       'bank_ks', 'bank_rs', 'ogrnip_number', 'email')
    extra = 0
    tab = True
    show_change_link = False
    can_delete = False


class JurAuthorInline(admin.StackedInline):
    model = LLCAuthor
    verbose_name = _('Верификационные данные')
    fields = ('name', 'name_short', 'director_name', 'director_short_name', 'buhgaler_name',
              'buhgaler_short_name', 'kpp', 'okpo', 'registration_date', 'oktmo',
              'ogrn', 'inn', 'contact_number', 'bank_name',
              'bank_bik', 'bank_ks', 'bank_rs', 'email')
    readonly_fields = ('name', 'name_short', 'director_name', 'director_short_name', 'buhgaler_name',
                       'buhgaler_short_name', 'kpp', 'okpo', 'registration_date', 'oktmo',
                       'ogrn', 'inn', 'contact_number', 'bank_name',
                       'bank_bik', 'bank_ks', 'bank_rs', 'email')
    extra = 0
    tab = True
    show_change_link = False
    can_delete = False

##############################################################################################################
# Admin Models
##############################################################################################################
@register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('email_link', 'title_display', 'author_type', 'full_name', 'email_is_verified', 'verification_status',
                    'is_active', 'last_login')
    list_editable = ('email_is_verified', 'verification_status', 'is_active')
    ordering = ('title',)

    search_fields = ('title', 'email', 'first_name', 'last_name', 'middle_name')
    list_filter_submit = True
    list_filter = ('author_type', 'is_premium_partner', 'verification_status', 'email_is_verified', 'is_active',
                   ('last_login', RangeDateTimeFilter))

    readonly_fields = ('last_login', 'full_name')
    fieldsets = (
        (_('Статус'), {'fields': ('is_premium_partner', 'verification_status', 'is_active', 'deactivation_reason',
                                  'last_login')}),
        (_('Контакты'), {'fields': ('email', 'email_is_verified', 'phone_number', 'region', 'address',
                                    'legal_address', 'website')}),
        (_('Профиль'), {'fields': ('photo', 'first_name', 'last_name', 'middle_name', 'bio', 'logo', 'title',
                                   'full_title', 'alias', 'prepositional_title', 'genitive_title',
                                   'description', 'education_type')}),
    )

    inlines = (DocumentInline, CourseInline, SchoolInline, PaymentInline)
    formfield_overrides = {
        models.TextField: {'widget': WysiwygWidget},
    }


    @display(
        description='ФИО',
        ordering=Concat('last_name', Value(' '), 'first_name', Value(' '), 'middle_name'),
        empty_value='-',
    )
    def full_name(self, obj):
        return f'{obj.last_name} {obj.first_name} {obj.middle_name}'

    @display(
        description='Email',
        ordering='email',
    )
    def email_link(self, obj):
        if obj.email:
            return format_html('<a href="{}">{}</a>', 
                           reverse('admin:author_author_change', args=[obj.pk]), 
                           obj.email)
        return "-"

    @display(
        description='Название',
        ordering='title',
    )
    def title_display(self, obj):
        return obj.title

    def get_queryset(self, request):
        return super().get_queryset(request).filter(organization__isnull=True)

    def get_inline_instances(self, request, obj=None):
        inlines = list(super().get_inline_instances(request, obj))

        if obj:
            if obj.author_type == AuthorType.INDIVIDUAL:
                inlines.append(FizAuthorInline(self.model, self.admin_site))
            elif obj.author_type == AuthorType.INDIVIDUAL_ENTREPRENEUR:
                inlines.append(FOPAuthorInline(self.model, self.admin_site))
            elif obj.author_type == AuthorType.ORGANIZATION:
                inlines.append(JurAuthorInline(self.model, self.admin_site))

        return inlines


@register(DocumentType)
class DocumentTypeAdmin(admin.ModelAdmin):
    list_display = ('name',)
    ordering = ('document_type',)

    search_fields = ('document_type',)

    readonly_fields = ('name',)
    fields = ('document_type',)

    @display(description='Название', ordering='document_type')
    def name(self, obj):
        return obj.document_type


@register(RequiredDocument)
class RequiredDocumentAdmin(admin.ModelAdmin):
    list_display = ('__str__',)
    filter_horizontal = ('document_types',)
    fields = ('author_type', 'document_types')
