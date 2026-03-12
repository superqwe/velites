from django.contrib import admin

from .models import Evento, Campo, Presenza, Attivita


@admin.register(Evento)
class EventoAdmin(admin.ModelAdmin):
    list_display = ('data', 'conferma','orario', 'attivita', 'campo', 'note')
    list_filter = ('attivita',)
    ordering = ('-data',)
    search_fields = ('data',)


@admin.register(Presenza)
class PresenzaAdmin(admin.ModelAdmin):
    list_display = ('evento__data','evento__attivita', 'evento__campo', 'utente', 'risposta')
    list_filter = ('utente', 'risposta')
    ordering = ( 'evento__data', 'risposta', 'utente' )


admin.site.register(Attivita)
admin.site.register(Campo)
