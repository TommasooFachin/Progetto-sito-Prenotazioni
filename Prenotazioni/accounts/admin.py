from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Account, Campo, Polisportiva, Prenotazione

class AccountAdmin(UserAdmin):
    model = Account
    list_display = ('email', 'nome', 'cognome', 'is_societario', 'is_active', 'is_staff')
    list_filter = ('is_societario', 'is_active', 'is_staff')
    fieldsets = (
        (None, {'fields': ('email', 'password', 'nome', 'cognome', 'is_societario', 'polisportiva')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'nome', 'cognome', 'password1', 'password2', 'is_societario', 'polisportiva', 'is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}
        ),
    )
    search_fields = ('email',)
    ordering = ('email',)

admin.site.register(Account, AccountAdmin)
admin.site.register(Polisportiva)
admin.site.register(Campo)
admin.site.register(Prenotazione)