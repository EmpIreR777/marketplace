from django.contrib.admin import register
from django.utils.translation import gettext as _
from unfold import admin
from unfold.contrib.filters.admin import RangeDateTimeFilter

from author.admin import DocumentInline, CourseInline, SchoolInline
from organizations.models import Organization, OrganizationRequisites
from userauth.admin import PaymentInline


##############################################################################################################
# Inlines
##############################################################################################################
class RequisitesInline(admin.StackedInline):
    model = OrganizationRequisites
    max_num = 1
    extra = 1
    tab = True


##############################################################################################################
# Admin Models
##############################################################################################################
@register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    list_display = ('title', 'type', 'email', 'email_is_verified', 'is_verified', 'is_active', 'last_login')
    search_fields = ('title', 'type', 'email')
    readonly_fields = ('last_login',)

    fieldsets = (
        (_('Статус'), {'fields': ('is_premium_partner', 'partner_card', 'is_verified', 'is_active',
                                  'deactivation_reason', 'last_login')}),
        (_('Контакты'), {'fields': ('email', 'email_is_verified', 'phone_number', 'region', 'address',
                                    'legal_address', 'website')}),
        (_('Профиль'), {'fields': ('logo', 'title', 'full_title', 'alias', 'prepositional_title',
                                   'genitive_title', 'description', 'license')}),
        (_('Дополнительно'), {'fields': ('leadership', 'personal_account_name', 'personal_account_site')})
    )

    ordering = ('title',)

    list_filter_submit = True
    list_filter = ('is_premium_partner', 'is_premium_partner', 'is_verified', 'email_is_verified',
                   'is_active', 'type', ('last_login', RangeDateTimeFilter))

    inlines = (DocumentInline, RequisitesInline, CourseInline, SchoolInline, PaymentInline)
