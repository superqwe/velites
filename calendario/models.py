import datetime

from django.contrib.auth import get_user_model
from django.db import models

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
    conferma = models.CharField(
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

    class Meta:
        unique_together = ('evento', 'utente')

        ordering = ['evento', 'utente']
        verbose_name_plural = 'Presenze'
        verbose_name = 'Presenza'

    def __str__(self):
        return f'{self.evento} - {self.utente} - {self.risposta}'
