from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    nickname = models.CharField(max_length=100, null=True, blank=True)
    calendario_aggiungi_presenza = models.BooleanField(default=True)

