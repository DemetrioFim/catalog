# ecommerce_catalog/ecommerce_catalog/urls.py

from django.contrib import admin
from django.urls import path, include  # Inclua o include para adicionar as URLs do app

urlpatterns = [
    path('admin/', admin.site.urls),  # URL padrão do admin
    path('accounts/', include('django.contrib.auth.urls')),
    path('', include('products.urls')),  # Inclua as URLs do app 'products'
]
