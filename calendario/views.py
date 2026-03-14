import datetime

from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.shortcuts import redirect

from .models import Evento, Presenza


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


def evento(request, id):
    evento = get_object_or_404(Evento, pk=id)

    presenze = evento.partecipazioni.all().order_by('utente__username')

    if request.method == 'POST':
        presenza_id = request.POST.get('salva')
        nuova_risposta = request.POST.get(f'risposta_{presenza_id}')
        nuova_nota = request.POST.get(f'nota_{presenza_id}')

        presenza = get_object_or_404(Presenza, pk=presenza_id)
        presenza.risposta = nuova_risposta
        presenza.nota = nuova_nota
        presenza.save()

    context = {
        "evento": evento,
        "presenze": presenze,
    }

    if prossimo_evento_id() == evento.pk:
        context["pagina_attiva_prossimo_evento"] = 'active'

    return render(request, "calendario/evento.html", context)
