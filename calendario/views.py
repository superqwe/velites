from django.http import HttpResponse
from .models import Evento
from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render



def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")


def calendario(request):
    eventi = Evento.objects.all().order_by('data')
    context = {'eventi': eventi}

    return render(request, 'calendario/elenco_eventi.html', context)
