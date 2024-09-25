# ecommerce_catalog/middleware.py

from django.shortcuts import redirect
from django.urls import reverse
from django.utils.deprecation import MiddlewareMixin

class LoginRequiredMiddleware(MiddlewareMixin):
    """
    Middleware que requer autenticação para todas as views, exceto para as URLs listadas em 'excluded_urls'.
    """

    def process_view(self, request, view_func, view_args, view_kwargs):
        # URLs que não requerem autenticação
        excluded_urls = [
            reverse('login'),
            reverse('logout'),
            # Adicione outras URLs públicas aqui se necessário
        ]

        # Verifica se a URL atual está na lista de exceções
        if not request.user.is_authenticated and request.path not in excluded_urls:
            return redirect('login')

        return None
