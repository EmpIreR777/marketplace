import re

from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError


def validate_payment_card(value):
    if not re.fullmatch(r'^\d{4}-\d{4}-\d{4}-\d{4}$', value):
        raise ValidationError(_('Номер карты должен быть в формате XXXX-XXXX-XXXX-XXXX.'))


def validate_bank_account(value):
    if not re.fullmatch(r'^\d{20}$', value):
        raise ValidationError(_('Банковский счёт должен содержать 20 цифр без пробелов.'))