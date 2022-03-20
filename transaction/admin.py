from django.contrib import admin

from .models import Transaction


class TransactionAdmin(admin.ModelAdmin):
    list_display = ('payer', 'payee', 'amount', 'created',)
    list_filter = ('payer', 'payee', 'amount', 'created',)

    search_fields = ('payer',)
    ordering = ('created',)


admin.site.register(Transaction, TransactionAdmin)
