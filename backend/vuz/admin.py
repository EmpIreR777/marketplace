import json
from django.contrib import admin
from django.contrib.admin import register
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _
from unfold import admin
from unfold.contrib.filters.admin import RangeDateFilter

from vuz.models import (
    AdmissionOffices, Cities, Contacts, Directions,
    Metros, Subjects, OrganizationsVuz, Faculties, 
    Forms, Professions, Specialties, Programs
)


##############################################################################################################
# Base Admin Class
##############################################################################################################
class VuzBaseAdmin(admin.ModelAdmin):
    """Базовый класс админки для моделей с полями type и source"""
    list_display = ('id', 'type', 'source', 'created_at', 'updated_at')
    list_filter = ('type', 'source', ('created_at', RangeDateFilter), ('updated_at', RangeDateFilter))
    search_fields = ('id',)
    readonly_fields = ('id', 'created_at', 'updated_at')
    list_per_page = 20
    
    def get_list_display(self, request):
        """Динамически добавляем name в list_display, если оно есть в модели"""
        list_display = list(super().get_list_display(request))
        if hasattr(self.model, 'name'):
            list_display.insert(1, 'name')
        return list_display
    
    def get_search_fields(self, request):
        """Динамически добавляем name в search_fields, если оно есть в модели"""
        search_fields = list(super().get_search_fields(request))
        if hasattr(self.model, 'name'):
            search_fields.append('name')
        return search_fields
    
    def get_readonly_fields(self, request, obj=None):
        """Динамически добавляем external_updated_at в readonly_fields, если оно есть в модели"""
        readonly_fields = list(super().get_readonly_fields(request, obj))
        if hasattr(self.model, 'external_updated_at'):
            readonly_fields.append('external_updated_at')
        return readonly_fields
    
    def get_fieldsets(self, request, obj=None):
        """Базовые fieldsets для моделей с type и source"""
        fieldsets = [
            (_('Основная информация'), {'fields': ['id', 'type', 'source']}),
        ]
        
        # Добавляем name в основную информацию, если оно есть
        if hasattr(self.model, 'name'):
            fieldsets[0][1]['fields'].append('name')
            
        # Создаем список полей для раздела "Даты"
        date_fields = ['created_at', 'updated_at']
        if hasattr(self.model, 'external_updated_at'):
            date_fields.append('external_updated_at')
            
        fieldsets.append((_('Даты'), {'fields': date_fields}))
        
        return fieldsets
    
    def get_ordering(self, request):
        """Динамическая сортировка по полю name, если оно есть"""
        if hasattr(self.model, 'name'):
            return ['name']
        return ['id']

    def format_json(self, json_data):
        """Форматирует JSON для лучшего отображения в админке"""
        if not json_data:
            return '-'
        
        if isinstance(json_data, str):
            try:
                json_data = json.loads(json_data)
            except json.JSONDecodeError:
                return json_data
        
        try:
            formatted_json = json.dumps(json_data, indent=2, ensure_ascii=False)
            return mark_safe(f'<pre>{formatted_json}</pre>')
        except:
            return str(json_data)


##############################################################################################################
# Admin Models
##############################################################################################################
@register(AdmissionOffices)
class AdmissionOfficesAdmin(VuzBaseAdmin):
    list_display = ('id', 'type', 'source', 'site', 'email', 'address', 'created_at')
    search_fields = ('id', 'site', 'email', 'address', 'post_index')
    readonly_fields = ('id', 'created_at', 'updated_at', 'external_updated_at', 'display_phones', 'display_schedule')
    
    def get_fieldsets(self, request, obj=None):
        fieldsets = super().get_fieldsets(request, obj)
        fieldsets.append(
            (_('Контактная информация'), {'fields': ('site', 'email', 'phones', 'display_phones', 'address', 
                                                     'longitude_latitude', 'post_index')})
        )
        fieldsets.append(
            (_('Расписание'), {'fields': ('schedule', 'display_schedule', 'description', 'start_date', 'end_date', 'is_full_year')})
        )
        return fieldsets
    
    def display_phones(self, obj):
        """Отображение телефонов в читаемом виде"""
        return self.format_json(obj.phones)
    display_phones.short_description = "Телефоны (форматированные)"
    
    def display_schedule(self, obj):
        """Отображение расписания в читаемом виде"""
        return self.format_json(obj.schedule)
    display_schedule.short_description = "Расписание (форматированное)"


@register(Cities)
class CitiesAdmin(VuzBaseAdmin):
    list_display = ('id', 'name', 'name_rp', 'type', 'source', 'is_capital', 'city_type')
    search_fields = ('id', 'name', 'name_rp', 'fias_id', 'kladr_id')
    list_filter = ('is_capital', 'city_type', 'ratio_population', 'type', 'source')
    readonly_fields = ('id', 'created_at', 'updated_at', 'display_calculation_data')
    
    def get_fieldsets(self, request, obj=None):
        fieldsets = super().get_fieldsets(request, obj)
        fieldsets.append(
            (_('Дополнительная информация'), {'fields': ('name_rp', 'is_capital', 'city_type', 
                                                        'ratio_population', 'longitude_latitude')})
        )
        fieldsets.append(
            (_('Идентификаторы'), {'fields': ('fias_id', 'kladr_id')})
        )
        fieldsets.append(
            (_('Расчетные данные'), {'fields': ('calculation_data', 'display_calculation_data')})
        )
        return fieldsets
    
    def display_calculation_data(self, obj):
        """Отображение расчетных данных в читаемом виде"""
        return self.format_json(obj.calculation_data)
    display_calculation_data.short_description = "Расчетные данные (форматированные)"


@register(Contacts)
class ContactsAdmin(VuzBaseAdmin):
    list_display = ('id', 'type', 'source', 'site', 'email', 'address', 'created_at')
    search_fields = ('id', 'site', 'email', 'address', 'post_index')
    readonly_fields = ('id', 'created_at', 'updated_at', 'display_phones')
    
    def get_fieldsets(self, request, obj=None):
        fieldsets = super().get_fieldsets(request, obj)
        fieldsets.append(
            (_('Контактная информация'), {'fields': ('address', 'post_index', 'site', 'phones', 'display_phones', 'email')})
        )
        return fieldsets
    
    def display_phones(self, obj):
        """Отображение телефонов в читаемом виде"""
        if not obj.phones:
            return "-"
        
        if hasattr(obj.phones, '__iter__') and not isinstance(obj.phones, str):
            return ", ".join(obj.phones)
        return obj.phones
    display_phones.short_description = "Телефоны (форматированные)"


@register(Directions)
class DirectionsAdmin(VuzBaseAdmin):
    list_display = ('id', 'name', 'code', 'type', 'source', 'organization_type')
    search_fields = ('id', 'name', 'code', 'synonym')
    list_filter = ('organization_type', 'type', 'source')
    readonly_fields = ('id', 'created_at', 'updated_at', 'display_calculation_data')
    
    def get_fieldsets(self, request, obj=None):
        fieldsets = super().get_fieldsets(request, obj)
        fieldsets.append(
            (_('Дополнительная информация'), {'fields': ('code', 'synonym', 'organization_type')})
        )
        fieldsets.append(
            (_('Расчетные данные'), {'fields': ('calculation_data', 'display_calculation_data')})
        )
        return fieldsets
    
    def display_calculation_data(self, obj):
        """Отображение расчетных данных в читаемом виде"""
        return self.format_json(obj.calculation_data)
    display_calculation_data.short_description = "Расчетные данные (форматированные)"


@register(Metros)
class MetrosAdmin(VuzBaseAdmin):
    list_display = ('id', 'name', 'type', 'source', 'created_at')
    search_fields = ('id', 'name')


@register(Subjects)
class SubjectsAdmin(VuzBaseAdmin):
    list_display = ('id', 'code', 'type', 'source', 'subject_type')
    search_fields = ('id', 'name', 'code', 'fias_id', 'kladr_id')
    list_filter = ('subject_type',)
    
    def get_fieldsets(self, request, obj=None):
        fieldsets = super().get_fieldsets(request, obj)
        fieldsets.append(
            (_('Дополнительная информация'), {'fields': ('name_rp', 'code', 'subject_type')})
        )
        fieldsets.append(
            (_('Идентификаторы'), {'fields': ('fias_id', 'kladr_id')})
        )
        return fieldsets


@register(OrganizationsVuz)
class OrganizationsVuzAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'short_name', 'type', 'source', 'published', 'is_state', 'city', 'display_logo')
    list_filter = ('published', 'is_state', 'is_hostel', 'is_military', 'is_departmental', 
                 'is_partner', 'has_leads', 'is_confirmed', 'is_top100', 'organization_type', 
                 'obrnadzor_checked', ('created_at', RangeDateFilter), ('updated_at', RangeDateFilter))
    search_fields = ('id', 'name', 'full_name', 'short_name', 'code', 'inn')
    readonly_fields = ('id', 'created_at', 'updated_at', 'external_updated_at', 'display_logo', 'format_calculation_data')
    autocomplete_fields = ('city', 'subject', 'metro', 'contact', 'admission_office')
    list_per_page = 20
    
    fieldsets = (
        (_('Основная информация'), {'fields': ('id', 'type', 'source', 'name', 'code', 'full_name', 'short_name', 
                                             'organization_type', 'sub_type', 'site')}),
        (_('SEO и описание'), {'fields': ('obrnadzor_name', 'short_seo', 'about', 'logo', 'logo_storage', 'display_logo', 'video_link')}),
        (_('Статусы'), {'fields': ('published', 'is_state', 'is_hostel', 'is_military', 'is_departmental', 
                                'is_partner', 'has_leads', 'is_confirmed', 'is_top100')}),
        (_('Сортировка'), {'fields': ('sort', 'sort_for_region', 'sort_for_top')}),
        (_('Реквизиты'), {'fields': ('inn', 'kpp', 'monitoring_code', 'longitude_latitude')}),
        (_('Лицензии и аккредитация'), {'fields': ('licence_num', 'licence_date', 'accreditation_number', 
                                              'accreditation_date', 'obrnadzor_checked')}),
        (_('Рейтинги и показатели'), {'fields': ('rating', 'esi', 'esi24', 'esi_marks', 'ege_score', 'cost')}),
        (_('Связи'), {'fields': ('city', 'subject', 'metro', 'contact', 'admission_office')}),
        (_('Дополнительные данные'), {'fields': ('old_names', 'delete_reason', 'confirmed_and_date', 'format_calculation_data')}),
        (_('Даты'), {'fields': ('created_at', 'updated_at', 'external_updated_at')}),
    )
    
    def display_logo(self, obj):
        """Отображение логотипа организации"""
        if not obj.logo:
            return "-"
        return format_html('<img src="{}" width="100" />', obj.logo)
    display_logo.short_description = "Логотип"
    
    def format_calculation_data(self, obj):
        """Отображение расчетных данных в читаемом виде"""
        if not obj.calculation_data:
            return "-"
        
        try:
            formatted_json = json.dumps(obj.calculation_data, indent=2, ensure_ascii=False)
            return mark_safe(f'<pre>{formatted_json}</pre>')
        except:
            return str(obj.calculation_data)
    format_calculation_data.short_description = "Расчетные данные (форматированные)"


@register(Faculties)
class FacultiesAdmin(VuzBaseAdmin):
    list_display = ('id', 'name', 'code', 'type', 'source', 'organization_vuz')
    search_fields = ('id', 'name', 'code', 'address', 'email', 'phone')
    list_filter = ('type', 'source')
    autocomplete_fields = ('organization_vuz',)
    readonly_fields = ('id', 'created_at', 'updated_at', 'display_calculation_data')
    
    def get_fieldsets(self, request, obj=None):
        fieldsets = super().get_fieldsets(request, obj)
        fieldsets.append(
            (_('Дополнительная информация'), {'fields': ('code', 'organization_vuz')})
        )
        fieldsets.append(
            (_('Контактная информация'), {'fields': ('post_index', 'address', 'email', 'phone', 'longitude_latitude')})
        )
        fieldsets.append(
            (_('Расчетные данные'), {'fields': ('calculation_data', 'display_calculation_data')})
        )
        return fieldsets
    
    def display_calculation_data(self, obj):
        """Отображение расчетных данных в читаемом виде"""
        return self.format_json(obj.calculation_data)
    display_calculation_data.short_description = "Расчетные данные (форматированные)"


@register(Forms)
class FormsAdmin(VuzBaseAdmin):
    list_display = ('id', 'name', 'type', 'source', 'created_at')
    search_fields = ('id', 'name')


@register(Professions)
class ProfessionsAdmin(VuzBaseAdmin):
    list_display = ('id', 'name', 'code', 'type', 'source', 'published', 'organization_type')
    list_filter = ('published', 'organization_type', 'type', 'source')
    search_fields = ('id', 'name', 'code', 'slug', 'short_text')
    readonly_fields = ('id', 'created_at', 'updated_at', 'external_updated_at', 'display_extra_names')
    
    def get_fieldsets(self, request, obj=None):
        fieldsets = super().get_fieldsets(request, obj)
        fieldsets.append(
            (_('Статус'), {'fields': ('published',)})
        )
        fieldsets.append(
            (_('Дополнительная информация'), {'fields': ('code', 'slug', 'organization_type')})
        )
        fieldsets.append(
            (_('Содержание'), {'fields': ('short_text', 'full_text', 'other_text_1', 'other_text_2', 'extra_names', 'display_extra_names')})
        )
        fieldsets.append(
            (_('Медиа'), {'fields': ('preview_image', 'detail_image')})
        )
        return fieldsets
    
    def display_extra_names(self, obj):
        """Отображение дополнительных названий в читаемом виде"""
        return self.format_json(obj.extra_names)
    display_extra_names.short_description = "Дополнительные названия (форматированные)"


@register(Specialties)
class SpecialtiesAdmin(VuzBaseAdmin):
    list_display = ('id', 'name', 'code', 'qualification', 'type', 'source')
    search_fields = ('id', 'name', 'code', 'code_okso', 'code_old', 'code_okso_new', 'qualification')
    list_filter = ('level_code', 'type', 'source')
    readonly_fields = ('id', 'created_at', 'updated_at', 'display_calculation_data')
    
    def get_fieldsets(self, request, obj=None):
        fieldsets = super().get_fieldsets(request, obj)
        fieldsets.append(
            (_('Дополнительная информация'), {'fields': ('qualification', 'description', 'description_work')})
        )
        fieldsets.append(
            (_('Коды'), {'fields': ('code', 'code_okso', 'code_old', 'code_okso_new', 'level_code')})
        )
        fieldsets.append(
            (_('Расчетные данные'), {'fields': ('calculation_data', 'display_calculation_data')})
        )
        return fieldsets
    
    def display_calculation_data(self, obj):
        """Отображение расчетных данных в читаемом виде"""
        return self.format_json(obj.calculation_data)
    display_calculation_data.short_description = "Расчетные данные (форматированные)"


@register(Programs)
class ProgramsAdmin(admin.ModelAdmin):
    list_display = ('id', 'profile', 'type', 'source', 'organization_vuz', 'specialty', 'form', 'duration', 'cost')
    search_fields = ('id', 'profile', 'organization_vuz__name', 'specialty__name')
    list_filter = ('type', 'source', ('created_at', RangeDateFilter), ('updated_at', RangeDateFilter))
    autocomplete_fields = ('organization_vuz', 'faculty', 'specialty', 'form')
    readonly_fields = ('id', 'created_at', 'updated_at', 'display_calculation_data')
    list_per_page = 20
    
    fieldsets = (
        (_('Основная информация'), {'fields': ('id', 'type', 'source', 'profile')}),
        (_('Связи'), {'fields': ('organization_vuz', 'faculty', 'specialty', 'form')}),
        (_('Характеристики программы'), {'fields': ('duration', 'budget_places', 'budget_score', 
                                              'commercial_places', 'commercial_score', 'cost')}),
        (_('Расчетные данные'), {'fields': ('calculation_data', 'display_calculation_data')}),
        (_('Даты'), {'fields': ('created_at', 'updated_at')}),
    )
    
    def display_calculation_data(self, obj):
        """Отображение расчетных данных в читаемом виде"""
        if not obj.calculation_data:
            return "-"
        
        try:
            formatted_json = json.dumps(obj.calculation_data, indent=2, ensure_ascii=False)
            return mark_safe(f'<pre>{formatted_json}</pre>')
        except:
            return str(obj.calculation_data)
    display_calculation_data.short_description = "Расчетные данные (форматированные)"
