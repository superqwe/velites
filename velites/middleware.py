from datetime import datetime
import sys

from django.shortcuts import redirect
from django.urls import reverse
from loguru import logger


class LoginRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.exempt_urls = [
            reverse('login'),
            reverse('logout'),
            '/admin/login/',
        ]

    def __call__(self, request):
        if (
                not request.user.is_authenticated
                and request.path not in self.exempt_urls
                and not request.path.startswith('/admin/')
        ):
            return redirect('login')

        return self.get_response(request)


class DjangoLoguruMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        logger.remove()
        # logger.add(sys.stderr, format="{message}", colorize=True)
        logger.add("logs/django.log", format="{message}", rotation="10 MB", retention="30 days")

    def __call__(self, request):
        response = self.get_response(request)

        if hasattr(request, 'user') and request.user.is_authenticated:
            user = request.user.username
        else:
            user = "anonimo"

        tempo = datetime.now().strftime("[%d/%b/%Y %H:%M:%S]")
        logger.info(f"{tempo} {request.method} {request.build_absolute_uri()} - utente: {user} - status: {response.status_code}")

        return response
