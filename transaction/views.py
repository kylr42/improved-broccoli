from django.core.exceptions import ValidationError
from django.shortcuts import render
from django.http import HttpResponseRedirect
from .forms import Payment
from .models import Customer
from django.db import transaction


def process_payment(request):
    if request.method == 'POST':

        form = Payment(request.POST)

        if form.is_valid():
            x = form.cleaned_data['payer']
            y = form.cleaned_data['payee']
            z = form.cleaned_data['amount']

            payer = Customer.objects.select_for_update().get(name=x)
            payee = Customer.objects.select_for_update().get(name=y)

            with transaction.atomic():
                payer.balance -= z
                if payer.balance < 0:
                    raise ValidationError(
                        "Bad amount!"
                    )
                payer.save()

                payee.balance += z
                payee.save()

                return HttpResponseRedirect('/')

    else:
        form = Payment()

    return render(request, 'index.html', {'form': form})
