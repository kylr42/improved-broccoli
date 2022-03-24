from django.contrib import admin

from .models import Transaction, TransactionAccount


class TransactionAccountAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer', 'balance', 'is_active',)
    list_filter = ('id', 'customer', 'balance', 'is_active',)

    search_fields = ('id', 'customer',)
    ordering = ('id',)


class TransactionAdmin(admin.ModelAdmin):
    list_display = ('payer', 'payee', 'amount', 'created',)
    list_filter = ('payer', 'payee', 'amount', 'created',)

    search_fields = ('payer',)
    ordering = ('created',)


admin.site.register(TransactionAccount, TransactionAccountAdmin)
admin.site.register(Transaction, TransactionAdmin)

