from django.contrib import admin

from .models import Evento, Campo, Presenza, Attivita


@admin.register(Evento)
class EventoAdmin(admin.ModelAdmin):
    date_hierarchy = 'data'
    list_display = ('data', 'conferma', 'orario', 'attivita', 'campo', 'note')
    list_filter = ('conferma', 'attivita')
    ordering = ('-data',)
    search_fields = ('data',)


@admin.register(Presenza)
class PresenzaAdmin(admin.ModelAdmin):
    date_hierarchy = 'evento__data'
    list_display = ('evento__data', 'evento__attivita', 'evento__campo', 'utente__nickname', 'risposta')
    list_filter = ('risposta', 'utente',)
    ordering = ('-evento__data', 'risposta', 'utente__nickname')


admin.site.register(Attivita)
admin.site.register(Campo)
