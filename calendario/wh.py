import configparser
import os
from pathlib import Path

import requests

# APScheduler


config = configparser.ConfigParser()
config.read(os.path.join(Path(__file__).resolve().parent.parent, "config.cfg"))

WHAPI_TOKEN = config["whatsapp"]["token"]
# WHAPI_GROUP_ID = config["whatsapp"]["group_id_velites"]
WHAPI_GROUP_ID = config["whatsapp"]["group_id_cancella"]

GIORNO_SETTIMANA = [
    "Lunedì", "Martedì", "Mercoledì",
    "Giovedì", "Venerdì", "Sabato", "Domenica"
]


def invia_messaggio(evento, presenze):
    messaggio = formatta_messagio(evento, presenze)
    send_group_message(messaggio)
    # print(messaggio)


def formatta_messagio(evento, presenze):
    attivita = (f'*{evento.attivita} '
                f'{GIORNO_SETTIMANA[evento.data.weekday()]} '
                f'{evento.data.strftime('%d/%m/%y')}*')

    dove = f'{evento.campo} ore {evento.orario.strftime('%H:%M')}'

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

    messaggio = (f'{attivita}\n{dove}'
                 f'{presenti}'
                 f'{assenti}'
                 f'{forse}')

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
