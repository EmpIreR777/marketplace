from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class TariffsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'tariffs'
    verbose_name = _('Тарифы')
