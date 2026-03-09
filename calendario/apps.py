from django.apps import AppConfig


class CalendarioConfig(AppConfig):
    name = 'calendario'

    def ready(self):
        import calendario.signals
