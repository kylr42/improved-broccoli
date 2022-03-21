from django.db import transaction
from rest_framework.exceptions import ValidationError

from .models import Transaction, PersonalAccount
from rest_framework import serializers


class PersonalAccountSerializer(serializers.ModelSerializer):

    class Meta:
        model = PersonalAccount
        fields = ['id', 'customer', 'balance', 'is_active', ]


class TransactionSerializer(serializers.ModelSerializer):

    def validate(self, data):
        if data['payer'] == data['payee']:
            raise ValidationError({"payer": "Payer must not equal to payee"})
        return super().validate(data)

    def create(self, validated_data):
        account = PersonalAccount.objects.select_for_update()

        payer = account.get(id=validated_data['payer'].id)
        payee = account.get(id=validated_data['payee'].id)

        with transaction.atomic():
            payer.balance -= validated_data['amount']
            payee.balance += validated_data['amount']

            if payer.balance < 0:
                raise ValidationError(
                    {"amount": "Check your available balance and try again"},
                    code="invalid",
                )

            payer.save()
            payee.save()

            return Transaction.objects.create(**validated_data).save()

    class Meta:
        model = Transaction
        fields = ['payer', 'payee', 'amount', ]

