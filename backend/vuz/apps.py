from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class VuzConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'vuz'
    verbose_name = _('ВУЗы')
