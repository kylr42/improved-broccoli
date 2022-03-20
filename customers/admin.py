from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import CustomerCreationForm, CustomerChangeForm
from .models import Customer


class CustomerAdmin(UserAdmin):
    add_form = CustomerCreationForm
    form = CustomerChangeForm
    list_display = ('email', 'balance', 'is_staff', 'is_active',)
    list_filter = ('email', 'balance', 'is_staff', 'is_active',)
    fieldsets = (
        (None, {'fields': ('email', 'balance', 'password')}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'balance', 'password1', 'password2', 'is_staff', 'is_active')}
         ),
    )
    search_fields = ('email',)
    ordering = ('balance',)


admin.site.register(Customer, CustomerAdmin)
