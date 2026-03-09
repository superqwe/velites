from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    # Aggiunge i campi custom nella pagina di modifica
    fieldsets = UserAdmin.fieldsets + (
        ('Info aggiuntive', {'fields': ('nickname', 'calendario_aggiungi_presenza',)}),
    )
    list_display = UserAdmin.list_display + ('nickname', 'calendario_aggiungi_presenza',)
