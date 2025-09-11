from django.utils import timezone
from pytz import UTC

from django.core.exceptions import ValidationError


def validate_expire_date(value):
    if value.astimezone(UTC) < timezone.now():
        raise ValidationError('Expire datetime cannot be older than the current date.')
