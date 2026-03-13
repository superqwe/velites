from django.http import HttpResponse
from .models import Evento, Presenza
from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")


def calendario(request):
    eventi = Evento.objects.all().order_by('-data')
    context = {'eventi': eventi,
               'pagina_attiva_calendario_completo': 'active'}

    return render(request, 'calendario/calendario_completo.html', context)


def prossimo_evento(request):
    eventi = Evento.objects.all().order_by('-data')
    context = {'eventi': eventi,
               'pagina_attiva_prossimo_evento': 'active'}

    return render(request, 'calendario/calendario_completo.html', context)


# todo: obsoleto
# def evento2(request, id):
#     evento = get_object_or_404(Evento, pk=id)
#     # Tutte le presenze
#     presenze = evento.partecipazioni.all()
#
#     # Filtrate per risposta
#     presenti = evento.partecipazioni.filter(risposta=Presenza.Risposta.PARTECIPO)
#     assenti = evento.partecipazioni.filter(risposta=Presenza.Risposta.NON_PARTECIPO)
#     forse = evento.partecipazioni.filter(risposta=Presenza.Risposta.FORSE)
#     context = {'evento': evento,
#                'presenze': presenze,
#                'presenti': presenti,
#                'assenti': assenti,
#                'forse': forse
#                }
#
#     return render(request, 'calendario/evento.html', context)


def evento(request, id):
    evento = get_object_or_404(Evento, pk=id)
    presenze = evento.partecipazioni.all().order_by('utente__username')

    if request.method == 'POST':
        presenza_id = request.POST.get('salva')
        nuova_risposta = request.POST.get(f'risposta_{presenza_id}')

        presenza = get_object_or_404(Presenza, pk=presenza_id)
        presenza.risposta = nuova_risposta
        presenza.save()

    context = {
        "evento": evento,
        "presenze": presenze,
    }

    return render(request, "calendario/evento.html", context)
