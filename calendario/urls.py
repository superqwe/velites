from django.urls import path

from . import views

app_name = "calendario"

urlpatterns = [
    # path("", views.index, name="index"),
    path("", views.prossimo_evento, name="prossimo_evento"),
    path("completo/", views.calendario, name="completo"),
]
