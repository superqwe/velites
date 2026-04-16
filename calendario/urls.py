from django.urls import path

from . import views

app_name = "calendario"

urlpatterns = [
    # path("", views.index, name="index"),
    path("", views.prossimo_evento, name="prossimo_evento"),
    path("eventi_futuri/", views.eventi_futuri, name="eventi_futuri"),
    path("eventi_passati/", views.eventi_passati, name="eventi_passati"),
    path("evento/<int:id>/", views.evento, name="evento"),
    path("log/", views.log, name="log"),
]
