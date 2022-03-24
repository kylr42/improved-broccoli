import celery
from rest_framework.exceptions import ValidationError
from django.db import transaction

from .celery import app
from transaction.models import TransactionAccount, Transaction


class AtomicTask(celery.Task):

    def __call__(self, *args, **kwargs):
        transfer = Transaction.objects.get(id=kwargs.get('transfer_id'))

        try:
            with transaction.atomic():
                transfer.status = 3
                transfer.save()
                return super().__call__(*args, **kwargs)

        except ValidationError:
            transfer.status = 2
            transfer.save()
            raise ValidationError()
        

@app.task(base=AtomicTask)
def transaction_handler(payer_id, payee_id, transfer_id, amount):
    import decimal

    account = TransactionAccount.objects.select_for_update()

    payer = account.get(id=payer_id)
    payee = account.get(id=payee_id)

    payer.balance -= decimal.Decimal(amount)
    payee.balance += decimal.Decimal(amount)

    if payer.balance < 0:
        raise ValidationError(
            code="invalid",
        )

    payer.save()
    payee.save()
    return {
        "status": 200,
        "message": "Transaction success completed!"
    }
