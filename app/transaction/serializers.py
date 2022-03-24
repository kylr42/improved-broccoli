from rest_framework.exceptions import ValidationError
from rest_framework import serializers

from .models import Transaction, TransactionAccount


class TransactionAccountSerializer(serializers.ModelSerializer):

    class Meta:
        model = TransactionAccount
        fields = ['id', 'customer', 'balance', 'is_active', ]
        read_only_fields = ('id', 'balance', 'is_active')


class TransactionSerializer(serializers.ModelSerializer):

    def validate(self, data):
        if data['payer'] == data['payee']:
            raise ValidationError({"payer": "Payer must not equal to payee"})
        return super().validate(data)

    def create(self, validated_data):
        from core.tasks import transaction_handler

        transfer = Transaction.objects.create(**validated_data)
        transaction_handler.delay(
            payer_id=validated_data['payer'].id,
            payee_id=validated_data['payee'].id,
            amount=validated_data['amount'],
            transfer_id=transfer.id,
        )
        return transfer

    class Meta:
        model = Transaction
        fields = ['id', 'payer', 'payee', 'amount', 'status', 'created']
        read_only_fields = ('id', 'status', 'created')

