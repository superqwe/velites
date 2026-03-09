from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Evento, Presenza, User


@receiver(post_save, sender=Evento)
def associa_utenti_attivi(sender, instance, created, **kwargs):
    if created:
        utenti_attivi = User.objects.filter(is_active=True, calendario_aggiungi_presenza=True)
        Presenza.objects.bulk_create([
            Presenza(evento=instance, utente=u)
            for u in utenti_attivi
        ])
