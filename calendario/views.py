from django.http import HttpResponse
from .models import Evento
from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render



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