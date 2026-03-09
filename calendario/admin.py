from django.contrib import admin

from .models import Evento, Campo, Presenza, Attivita

admin.site.register(Attivita)
admin.site.register(Campo)
admin.site.register(Evento)
admin.site.register(Presenza)
