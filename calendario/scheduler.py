from datetime import date, timedelta
from datetime import datetime
from zoneinfo import ZoneInfo

from apscheduler.schedulers.background import BackgroundScheduler

from .models import Evento
from .wh import invia_messaggio

from icecream import ic


def test():
    print(f"ciao - {datetime.now().strftime('%H:%M:%S')}")


def messaggio_automatico(giorno_della_settimana='lunedi'):
    ic('*** messaggio_automatico ***')
    giorni = {
        'lunedi': 6,
        'venerdi': 2
    }

    oggi = date.today()
    tra_n_giorni = oggi + timedelta(days=giorni[giorno_della_settimana])  # giorni da lunedì a domenica

    evento = Evento.objects.filter(data=tra_n_giorni).first()

    if evento and evento.conferma != 'NO':
        presenze = evento.partecipazioni.all().order_by('utente__username')
        invia_messaggio(evento, presenze, msg_automatico=giorno_della_settimana)
        ic('*** messaggio_automatico2 ***')


def start():
    scheduler = BackgroundScheduler(timezone=ZoneInfo('Europe/Rome'))

    # scheduler.add_job(
    #     messaggio_automatico,
    #     'cron',
    #     day_of_week='mon',
    #     hour=9,
    #     minute=0,
    #     id='messaggio_automatico',
    #     replace_existing=True,
    #     kwargs={'giorno_della_settimana': 'lunedi'},
    # )
    #
    # scheduler.add_job(
    #     messaggio_automatico,
    #     'cron',
    #     day_of_week='fri',
    #     hour=9,
    #     minute=0,
    #     id='messaggio_automatico',
    #     replace_existing=True,
    #     kwargs={'giorno_della_settimana': 'venerdi'},
    # )

    # scheduler.add_job(
    #     test,
    #     'interval',
    #     seconds=10,
    #     id='test',
    #     replace_existing=True,
    # )

    # scheduler.add_job(
    #     messaggio_automatico,
    #     'interval',
    #     #     seconds=10,
    #     id='messaggio_automatico2',
    #     replace_existing=True,
    #     kwargs={'giorno_della_settimana': 'lunedi'},
    # )

    scheduler.start()
