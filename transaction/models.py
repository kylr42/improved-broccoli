import uuid

from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _


class PersonalAccount(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    customer = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='personal_account')
    balance = models.DecimalField(_('personal balance'), max_digits=6, decimal_places=2, default=0)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.id}"


class Transaction(models.Model):
    payer = models.ForeignKey(PersonalAccount, on_delete=models.PROTECT, related_name='paying')
    payee = models.ForeignKey(PersonalAccount, on_delete=models.PROTECT, related_name='receiving')
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.payer.customer.email
