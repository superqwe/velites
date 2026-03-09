from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    in_calendario = models.BooleanField(default=True)

