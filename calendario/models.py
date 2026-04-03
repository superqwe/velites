import datetime
from unittest import case

from django.contrib.auth import get_user_model
from django.db import models

from .wh import invia_messaggio, formatta_messagio, send_group_message

User = get_user_model()


class Campo(models.Model):
    campo = models.CharField(max_length=100)

    class Meta:
        ordering = ['campo']
        verbose_name_plural = 'Campi'
        verbose_name = 'Campo'

    def __str__(self):
        return self.campo


def get_campo_default():
    return Campo.objects.get(pk=1).pk


class Attivita(models.Model):
    attivita = models.CharField(max_length=100)

    class Meta:
        ordering = ['attivita']
        verbose_name_plural = 'Attività'
        verbose_name = 'Attività'

    def __str__(self):
        return self.attivita


def get_attivita_default():
    return Attivita.objects.get(pk=1).pk


class Evento(models.Model):
    class Conferma(models.TextChoices):
        CONFERMATO = 'SI', 'Confermato'
        DA_CONFERMARE = 'FORSE', 'Da Confermare'
        ANNULLATO = 'NO', 'Annulato'

    data = models.DateField()
    orario = models.TimeField(default=datetime.time(8, 15), null=True, blank=True)
    attivita = models.ForeignKey(Attivita, on_delete=models.CASCADE, default=get_campo_default,
                                 null=True, blank=True)
    conferma = models.CharField('Stato',
        max_length=5,
        choices=Conferma.choices,
        default=Conferma.DA_CONFERMARE,
        null=True,
        blank=True,
    )
    campo = models.ForeignKey(Campo, on_delete=models.CASCADE, default=get_campo_default,
                              null=True, blank=True)
    nolo_prova = models.IntegerField(default=0, null=True, blank=True)
    note = models.TextField(null=True, blank=True)

    def save(self, *args, **kwargs):
        conferma_cambiata = False
        vecchia_conferma = None

        if self.pk:
            vecchio = Evento.objects.get(pk=self.pk)
            if vecchio.conferma != self.conferma:
                conferma_cambiata = True
                vecchia_conferma = vecchio.conferma

        super().save(*args, **kwargs)

        if conferma_cambiata:
            self.gestisci_cambio_conferma()

    def gestisci_cambio_conferma(self):
        presenze = self.partecipazioni.all().order_by('utente__nickname')
        messaggio = formatta_messagio(self, presenze, conferma=self.conferma)
        # print(messaggio)
        send_group_message(messaggio)

    class Meta:
        ordering = ['data']
        verbose_name_plural = 'Eventi'
        verbose_name = 'Evento'

    def __str__(self):
        if self.campo is None:
            campo = '?'
        else:
            campo = self.campo.campo

        if self.attivita is None:
            attivita = '?'
        else:
            attivita = self.attivita
        return f'{self.data} - {attivita} - {campo}'

    @property
    def evento_passato(self):
        if self.data < datetime.date.today():
            return True
        return False

    @property
    def colore_evento(self):
        match self.conferma:
            case 'SI':
                return 'bg-success'
            case 'FORSE':
                return 'bg-primary'
            case 'NO':
                return 'bg-danger'

    @property
    def n_presenti(self):
        return self.partecipazioni.filter(risposta='SI').count()

    @property
    def n_assenti(self):
        return self.partecipazioni.filter(risposta='NO').count()

    @property
    def n_forse(self):
        return self.partecipazioni.filter(risposta='FORSE').count()

    @property
    def n_non_risposto(self):
        return self.partecipazioni.filter(risposta__isnull=True).count()


class Presenza(models.Model):
    class Risposta(models.TextChoices):
        PARTECIPO = 'SI', 'Presente'
        NON_PARTECIPO = 'NO', 'Assente'
        FORSE = 'FORSE', 'Presenza in forse'

    evento = models.ForeignKey(Evento, on_delete=models.CASCADE, related_name='partecipazioni')
    utente = models.ForeignKey(User, on_delete=models.CASCADE, related_name='partecipazioni')
    risposta = models.CharField(
        max_length=5,
        choices=Risposta.choices,
        null=True,  # null = utente non ha ancora risposto
        blank=True,
    )
    nota = models.CharField(max_length=100, null=True, blank=True)

    class Meta:
        unique_together = ('evento', 'utente')

        ordering = ['evento', 'utente']
        verbose_name_plural = 'Presenze'
        verbose_name = 'Presenza'

    def __str__(self):
        return f'{self.evento} - {self.utente} - {self.risposta}'
