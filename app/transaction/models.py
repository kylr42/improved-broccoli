import uuid

from django.core.validators import MinValueValidator
from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _


class TransactionAccountManager(models.Manager):

    def get_queryset(self):
        return super(
            TransactionAccountManager, self
        ).get_queryset().filter(is_active=True)


class TransactionAccount(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    customer = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name='personal_account'
    )
    balance = models.DecimalField(
        _('personal balance'),
        max_digits=12, decimal_places=2, default=0,
        validators=[MinValueValidator(0)]
    )
    is_active = models.BooleanField(default=True)
    accounts = TransactionAccountManager()

    def __str__(self):
        return f"{self.id}"


class Transaction(models.Model):
    STATUS_CHOICES = (
        (1, "Processing"),
        (2, "Fail"),
        (3, "Success"),
    )
    payer = models.ForeignKey(TransactionAccount, on_delete=models.PROTECT, related_name='paying')
    payee = models.ForeignKey(TransactionAccount, on_delete=models.PROTECT, related_name='receiving')
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    status = models.IntegerField(choices=STATUS_CHOICES, default=1)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.payer.customer.email
