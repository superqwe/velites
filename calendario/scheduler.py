from datetime import date, timedelta

from apscheduler.schedulers.background import BackgroundScheduler
from icecream import ic

from .models import Evento
from .wh import invia_messaggio

from datetime import datetime


def test():
    print(f"ciao - {datetime.now().strftime('%H:%M:%S')}")


def messaggio_automatico(giorno_della_settimana):
    giorni = {
        'lunedi': 6,
        'venerdi': 2
    }

    oggi = date.today()
    tra_n_giorni = oggi + timedelta(days=giorni[giorno_della_settimana])  # giorni da lunedì a domenica

    evento = Evento.objects.filter(data=tra_n_giorni).first()

    try:
        ic(tra_n_giorni, giorno_della_settimana, evento.conferma)
    except AttributeError:
        ic(tra_n_giorni, giorno_della_settimana, None)

    if evento and evento.conferma != 'NO':
        presenze = evento.partecipazioni.all().order_by('utente__username')
        invia_messaggio(evento, presenze, msg_automatico=giorno_della_settimana)


def start():
    scheduler = BackgroundScheduler()

    scheduler.add_job(
        messaggio_automatico,
        'cron',
        day_of_week='mon',
        hour=21,
        minute=55,
        id='messaggio_automatico',
        replace_existing=True,
        kwargs={'giorno_della_settimana': 'lunedi'},
    )

    scheduler.add_job(
        messaggio_automatico,
        'cron',
        day_of_week='fri',
        hour=21,
        minute=55,
        id='messaggio_automatico',
        replace_existing=True,
        kwargs={'giorno_della_settimana': 'venerdi'},
    )

    scheduler.add_job(
        messaggio_automatico,
        'interval',
        seconds=5,
        id='test',
        replace_existing=True,
        kwargs={'giorno_della_settimana': 'venerdi'},
    )

    scheduler.start()
