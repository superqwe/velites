from django.apps import AppConfig
import os

class CalendarioConfig(AppConfig):
    name = 'calendario'

    def ready(self):
        import calendario.signals

        if os.environ.get('RUN_MAIN') == 'true':
            from . import scheduler
            scheduler.start()