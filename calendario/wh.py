import configparser
import os
import socket
from pathlib import Path

import requests
from icecream import ic

from django.db.models import Q

config = configparser.ConfigParser()
config.read(os.path.join(Path(__file__).resolve().parent.parent, "config.cfg"))

WHAPI_TOKEN = config["whatsapp"]["token"]

NOME_COMPUTER = socket.gethostname()
if NOME_COMPUTER.lower() == 'desktop-8g2ro2g':
    WHAPI_GROUP_ID = config["whatsapp"]["group_id_cancella"]
else:
    WHAPI_GROUP_ID = config["whatsapp"]["group_id_velites"]

GIORNO_SETTIMANA = [
    "Lunedì", "Martedì", "Mercoledì",
    "Giovedì", "Venerdì", "Sabato", "Domenica"
]


def invia_messaggio(evento, presenze, msg_automatico=False):
    messaggio = formatta_messagio(evento, presenze, msg_automatico=msg_automatico)
    # send_group_message(messaggio)
    print(messaggio)


def formatta_messagio(evento, presenze, conferma=None, msg_automatico=False):
    if conferma == 'SI':
        stato = '*EVENTO CONFERMATO*\n'
    elif conferma == 'NO':
        stato = '*EVENTO ANNULLATO*\n'
    elif conferma == 'FORSE':
        stato = '*EVENTO DA CONFERMARE*\n'
    else:
        stato = ''

    attivita = (f'*{evento.attivita} '
                f'{GIORNO_SETTIMANA[evento.data.weekday()]} '
                f'{evento.data.strftime('%d/%m/%y')}*')

    dove = f'{evento.campo} ore {evento.orario.strftime('%H:%M')}'

    note = f'Note: _{evento.note.replace('\n', '_ \n_')}_'

    intestazione = f'{stato}{attivita}\n{dove}\n{note}'

    if conferma == 'NO':
        return intestazione

    n_presenti = presenze.filter(risposta='SI').count()
    n_assenti = presenze.filter(risposta='NO').count()
    n_forse = presenze.filter(risposta='FORSE').count()

    presenti = '\n'.join(presenze.filter(risposta='SI').values_list('utente__nickname', flat=True))
    assenti = '\n'.join(presenze.filter(risposta='NO').values_list('utente__nickname', flat=True))
    forse = '\n'.join(presenze.filter(risposta='FORSE').values_list('utente__nickname', flat=True))

    if presenti:
        presenti = f'\n\n*PRESENTI - {n_presenti}*\n{presenti}'
    if assenti:
        assenti = f'\n\n*ASSENTI - {n_assenti}*\n{assenti}'
    if forse:
        forse = f'\n\n*IN FORSE - {n_forse}*\n{forse}'

    messaggio = (f'{intestazione}'
                 f'{presenti}'
                 f'{assenti}'
                 f'{forse}')

    match msg_automatico:
        case 'lunedi':
            messaggio = f'*POSTATE LE PRESENZE*\n{messaggio}'

        case 'venerdi':
            presenze_incerte = evento.partecipazioni.filter(Q(risposta='FORSE') | Q(risposta__isnull=True))
            ic(presenze_incerte)

            n_presenze_incerte = presenze_incerte.count()
            if n_presenze_incerte:
                msg_presenze_incerte = ', '.join(presenze_incerte.values_list('utente__nickname', flat=True))
                messaggio = f'{msg_presenze_incerte} forza con le presenze?'

    return messaggio


def send_group_message(message: str) -> bool:
    url = "https://gate.whapi.cloud/messages/text"
    headers = {
        "Authorization": f"Bearer {WHAPI_TOKEN}",
        "Content-Type": "application/json"
    }
    payload = {
        "to": WHAPI_GROUP_ID,
        "body": message
    }
    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()
        return True
    except requests.RequestException as e:
        print(f"Errore invio WhatsApp: {e}")
        return False
