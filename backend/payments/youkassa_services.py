import uuid
import logging
from yookassa import Payment, Configuration, Refund
from django.conf import settings

logger = logging.getLogger(__name__)


def _configure_yookassa():
    """Lazy configure YooKassa SDK. Must be called before any API call."""
    shop_id = settings.YOOKASSA_SHOP_ID
    secret_key = settings.YOOKASSA_SECRET_KEY

    if not shop_id or not secret_key:
        logger.warning(
            "YOOKASSA_SHOP_ID or YOOKASSA_SECRET_KEY is not set. "
            "YooKassa payments will fail."
        )

    Configuration.account_id = shop_id
    Configuration.secret_key = secret_key


def create_yokassa_payment(amount: float, description: str, payment_id: str):
    _configure_yookassa()
    idempotence_key = str(uuid.uuid4())
    payment = Payment.create({
        "amount": {
            "value": f"{amount:.2f}",
            "currency": "RUB"
        },
        "payment_method_data": {
            "type": "bank_card"
        },
        "confirmation": {
            "type": "redirect",
            "return_url": f"{settings.HOST_URL}/api/payments/{payment_id}/"
        },
        "description": description,
        "capture": True
    }, idempotence_key)

    return payment.confirmation.confirmation_url


def get_yokassa_payment_info(payment_id: str):
    _configure_yookassa()
    return Payment.find_one(payment_id)


def refund_yokassa_payment(amount: float, payment_id: str):
    _configure_yookassa()
    response = Refund.create({
        "amount": {
            "value": amount,
            "currency": "RUB"
        },
        "payment_id": payment_id
        })
    return response
