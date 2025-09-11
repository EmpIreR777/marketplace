from datetime import timedelta
from django.contrib.admin import SimpleListFilter, register, site
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.db.models import Value
from django.db.models.functions import Concat
from django.utils import timezone
from django.utils.translation import gettext as _
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from unfold import admin
from unfold.contrib.filters.admin import RangeDateTimeFilter
from unfold.decorators import display
from unfold.forms import AdminPasswordChangeForm, UserChangeForm, UserCreationForm

from payments.models import Payment

User = get_user_model()

site.unregister(Group)


##############################################################################################################
# Inlines
##############################################################################################################
class PaymentInline(admin.TabularInline):
    model = Payment
    fields = ('id', 'amount', 'payment_type', 'status', 'created_at')
    readonly_fields = ('id', 'created_at')
    extra = 0
    tab = True
    show_change_link = True
    can_delete = True


##############################################################################################################
# UserFilter
##############################################################################################################

class NewUserFilter(SimpleListFilter):
    title = _('Дата регистрации')
    parameter_name = 'registration_date'

    def lookups(self, request, model_admin):
        return (
            ('last_day', _('Последний день')),
            ('last_week', _('Последняя неделя')),
            ('last_month', _('Последний месяц')),
        )

    def queryset(self, request, queryset):
        now = timezone.now()
        if self.value() == 'last_day':
            return queryset.filter(created_at__gte=now - timedelta(days=1))
        if self.value() == 'last_week':
            return queryset.filter(created_at__gte=now - timedelta(weeks=1))
        if self.value() == 'last_month':
            return queryset.filter(created_at__gte=now - timedelta(days=30))
        return queryset
    
##############################################################################################################
# Admin Models
##############################################################################################################
@register(User)
class UserAdmin(BaseUserAdmin, admin.ModelAdmin):
    form = UserChangeForm
    add_form = UserCreationForm
    change_password_form = AdminPasswordChangeForm
    list_display = ('email', 'full_name', 'email_is_verified', 'is_staff', 'is_active', 'last_login')
    list_editable = ('email_is_verified', 'is_staff', 'is_active')
    ordering = ('email',)
    search_fields = ('email', 'first_name', 'last_name', 'middle_name')
    list_filter_submit = True
    list_filter = ('email_is_verified', 'is_staff', 'is_active', ('last_login', RangeDateTimeFilter), NewUserFilter)
    inlines = (PaymentInline,)

    filter_horizontal = ('groups', 'user_permissions')
    readonly_fields = ('last_login', 'full_name')
    fieldsets = (
        (_('Статус'), {'fields': ('is_active', 'deactivation_reason', 'last_login')}),
        (_('Контакты'), {'fields': ('email', 'email_is_verified', 'phone_number', 'region')}),
        (_('Профиль'), {'fields': ('photo', 'first_name', 'last_name', 'middle_name', 'bio')}),
        (_('Права'), {'fields': ('is_staff', 'groups', 'user_permissions')}),
        (_('Смена пароля'), {'fields': ('password',)}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )

    @display(
        description='ФИО',
        ordering=Concat('last_name', Value(' '), 'first_name', Value(' '), 'middle_name'),
        empty_value='-',
    )
    def full_name(self, obj):
        return f'{obj.last_name} {obj.first_name} {obj.middle_name}'

@register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ('name',)
    ordering = ('name',)
    filter_horizontal = ('permissions',)
    fields = ('name', 'permissions')
