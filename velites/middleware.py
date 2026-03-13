from django.shortcuts import redirect
from django.urls import reverse
from django.conf import settings

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
