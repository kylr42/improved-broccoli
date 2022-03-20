from django.db import models
from django.contrib.auth import get_user_model


class Transaction(models.Model):
    payer = models.ForeignKey(get_user_model(), on_delete=models.PROTECT, related_name='paying')
    payee = models.ForeignKey(get_user_model(), on_delete=models.PROTECT, related_name='receiving')
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    created = models.DateTimeField(auto_now_add=True)

    # def clean(self):
    #     if self.payer == self.payee:
    #         raise ValidationError({
    #                 "payer": "Payer should not be equal payee",
    #                 "payee": "Payee should not be equal payer"
    #             },
    #             code="invalid",
    #         )
    #     if self.payer.balance < self.amount:
    #         raise ValidationError(
    #             {"amount": "Check your available balance and try again"},
    #             code="error1",
    #         )
    #
    # def save(self, *args, **kwargs):
    #     with transaction.atomic():
    #         self.payer.balance -= self.amount
    #         self.payer.save()
    #
    #         self.payee.balance += self.amount
    #         self.payee.save()

    def __str__(self):
        return self.payer.email
