from django.contrib.admin import register
from django.utils.translation import gettext as _

from unfold import admin
from unfold.decorators import display

from tariffs.models import Tariff, UserTariff, TariffFeature


##############################################################################################################
# Inlines
##############################################################################################################
class TariffFeatureInline(admin.TabularInline):
    model = TariffFeature
    fields = ('id', 'text')
    extra = 1
    tab = True
    can_delete = True


##############################################################################################################
# Admin Models
##############################################################################################################
@register(UserTariff)
class UserTariffAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'tariff', 'is_paid', 'expire')

    search_fields = ('id', 'user__email', 'user__first_name', 'user__last_name', 'user__middle_name',
                     'tariff__name')
    list_filter_submit = True
    list_filter = ('is_paid', 'tariff__is_active', 'is_timeless')

    readonly_fields = ('id',)
    fieldsets = (
        (None, {'fields': ('id', 'user', 'tariff', 'is_paid', 'is_timeless', 'expire')}),
    )

    autocomplete_fields = ('user', 'tariff')


@register(Tariff)
class TariffAdmin(admin.ModelAdmin):
    list_display = ('name', 'percentage', 'discount', 'price', 'total_price', 'duration', 'is_show',
                    'is_active')
    list_editable = ('is_show', 'is_active')
    ordering = ('price',)

    search_fields = ('name',)
    list_filter_submit = True
    list_filter = ('is_show', 'is_active')

    readonly_fields = ('total_price',)
    fieldsets = (
        (_('Информация'), {'fields': ('name', 'duration', 'is_show', 'is_active')}),
        (_('Стоимость и оплата'), {'fields': ('percentage', 'price', 'discount', 'total_price')}),
    )

    inlines = (TariffFeatureInline,)

    @display(description='total price')
    def total_price(self, instance):
        return instance.total_price
