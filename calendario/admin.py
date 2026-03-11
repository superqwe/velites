from django.contrib import admin

from .models import Evento, Campo, Presenza, Attivita


@admin.register(Evento)
class EventoAdmin(admin.ModelAdmin):
    list_display = ('data', 'orario', 'attivita', 'campo')


@admin.register(Presenza)
class PresenzaAdmin(admin.ModelAdmin):
    list_display = ('evento__data','evento__attivita', 'evento__campo', 'utente', 'risposta')


admin.site.register(Attivita)
admin.site.register(Campo)
