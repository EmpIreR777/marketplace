import uuid
from yookassa import Payment, Configuration, Refund
from django.conf import settings


Configuration.account_id = settings.YOOKASSA_SHOP_ID
Configuration.secret_key = settings.YOOKASSA_SECRET_KEY


def create_yokassa_payment(amount: float, description: str, payment_id: str):
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
    return Payment.find_one(payment_id)


def refund_yokassa_payment(amount: float, payment_id: str):
    response = Refund.create({
        "amount": {
            "value": amount,
            "currency": "RUB"
        },
        "payment_id": payment_id
        })
    return response
