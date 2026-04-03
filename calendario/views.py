import datetime

from django.shortcuts import redirect
from django.shortcuts import render, get_object_or_404
from django.contrib import messages

from .models import Evento, Presenza
from .wh import invia_messaggio


def prossimo_evento_id():
    return Evento.objects.filter(data__gte=datetime.date.today()).order_by('data').first().pk


def eventi_futuri(request):
    eventi_futuri = Evento.objects.filter(data__gte=datetime.date.today()).order_by('data')
    context = {'eventi': eventi_futuri,
               'pagina_attiva_eventi_futuri': 'active'}

    return render(request, 'calendario/elenco_eventi.html', context)


def eventi_passati(request):
    eventi_passati = Evento.objects.filter(data__lt=datetime.date.today()).order_by('-data')
    context = {'eventi': eventi_passati,
               'pagina_attiva_eventi_passati': 'active'}

    return render(request, 'calendario/elenco_eventi.html', context)


def prossimo_evento(request):
    request.session['prossimo'] = 'active'

    return redirect('calendario:evento', id=prossimo_evento_id())


def evento2(request, id):
    # todo: obsoleto --> cancellare
    utente = request.user
    evento = get_object_or_404(Evento, pk=id)
    presenze = evento.partecipazioni.all().order_by('utente__username')
    messaggio_ok = False

    if request.method == 'POST':
        presenza_id = request.POST.get('salva')
        nuova_risposta = request.POST.get(f'risposta_{presenza_id}')
        nuova_nota = request.POST.get(f'nota_{presenza_id}')

        presenza = get_object_or_404(Presenza, pk=presenza_id)
        presenza.risposta = nuova_risposta
        presenza.nota = nuova_nota
        presenza.save()

        if prossimo_evento_id() == evento.pk:
            invia_messaggio(evento, presenze)

        messaggio_ok = True

    context = {
        "evento": evento,
        'utente': utente,
        "presenze": presenze,
        "messaggio_ok": messaggio_ok,
    }

    if prossimo_evento_id() == evento.pk:
        context["pagina_attiva_prossimo_evento"] = 'active'

    return render(request, "calendario/evento.html", context)


def evento(request, id):
    evento = get_object_or_404(Evento, pk=id)
    presenze_tutti = evento.partecipazioni.all().order_by('utente__username')
    presenze_altri_utenti = evento.partecipazioni.exclude(utente=request.user).order_by('utente__username')
    presenza_utente = Presenza.objects.filter(evento=evento, utente=request.user).first()
    is_gestore = request.user.groups.filter(name='Gestore').exists()

    if request.method == 'POST':

        if 'salva_conferma' in request.POST and is_gestore:
            nuova_conferma = request.POST.get('nuova_conferma')
            evento.conferma = nuova_conferma
            evento.save()
            messages.success(request, 'Stato evento aggiornato')
            return redirect('calendario:evento', id=id)

        elif 'salva' in request.POST:
            presenza_id = request.POST.get('salva')
            nuova_risposta = request.POST.get(f'risposta_{presenza_id}')
            nuova_nota = request.POST.get(f'nota_{presenza_id}')

            presenza = get_object_or_404(Presenza, pk=presenza_id)
            presenza.risposta = nuova_risposta
            presenza.nota = nuova_nota
            presenza.save()

            if prossimo_evento_id() == evento.pk:
                invia_messaggio(evento, presenze_tutti)

            messages.success(request, 'Presenza salvata')

            return redirect('calendario:evento', id=id)

    context = {
        "evento": evento,
        "presenze_altri_utenti": presenze_altri_utenti,
        "presenza_utente": presenza_utente,
        'presenze_tutti': presenze_tutti,
        'is_gestore': is_gestore,
    }

    if prossimo_evento_id() == evento.pk:
        context["pagina_attiva_prossimo_evento"] = 'active'

    return render(request, "calendario/evento.html", context)
