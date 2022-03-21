from rest_framework import viewsets

from .models import Transaction, PersonalAccount
from .serializers import TransactionSerializer, PersonalAccountSerializer


class PersonalAccountViewSet(viewsets.ModelViewSet):
    queryset = PersonalAccount.objects.all()
    serializer_class = PersonalAccountSerializer


class TransactionViewSet(viewsets.ModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer

