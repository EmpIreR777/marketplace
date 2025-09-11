import django_filters

from tariffs.models import Tariff


class TariffDurationTypeFilter(django_filters.FilterSet):
    class Meta:
        model = Tariff
        fields = ('duration',)
