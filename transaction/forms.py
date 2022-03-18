from django import forms
from django.core.exceptions import ValidationError


class Payment(forms.Form):
    payer = forms.CharField(max_length=30)
    payee = forms.CharField(max_length=30)
    amount = forms.DecimalField(max_digits=5, decimal_places=2)

    def clean(self):
        cleaned_data = super().clean()
        pay_er = cleaned_data.get("payer")
        pay_ee = cleaned_data.get("payee")

        if pay_er == pay_ee:
            raise ValidationError(
                "Bad payee!"
            )
