from django.contrib.auth import get_user_model
from django.db import transaction
from rest_framework.exceptions import ValidationError

from .models import Transaction
from rest_framework import serializers


class TransactionSerializer(serializers.ModelSerializer):

    def validate(self, data):
        if data['payer'] == data['payee']:
            raise ValidationError({"payer": "payer must not equal to payee"})
        return super().validate(data)

    def save(self, *args, **kwargs):
        User = get_user_model()
        data = self.validated_data
        payer = User.objects.select_for_update().get(id=data['payer'].id)
        payee = User.objects.select_for_update().get(id=data['payee'].id)

        with transaction.atomic():
            payer.balance -= data['amount']
            if payer.balance < 0:
                raise ValidationError(
                    {"amount": "Check your available balance and try again"},
                    code="invalid",
                )
            payer.save()

            payee.balance += data['amount']
            payee.save()

            Transaction.objects.create(**data)

    class Meta:
        model = Transaction
        fields = ['payer', 'payee', 'amount', ]

