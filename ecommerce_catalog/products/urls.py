# ecommerce_catalog/products/urls.py

# ecommerce_catalog/products/urls.py

from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', auth_views.LoginView.as_view(template_name='products/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),

    path('produtos/', views.lista_produtos, name='lista_produtos'),
    path('produtos/<int:produto_id>/editar/', views.editar_produto, name='editar_produto'),
    path('produtos/<int:produto_id>/excluir/', views.excluir_produto, name='excluir_produto'),

    path('clientes/', views.lista_clientes, name='lista_clientes'),
    path('clientes/<int:cliente_id>/editar/', views.editar_cliente, name='editar_cliente'),
    path('clientes/<int:cliente_id>/excluir/', views.excluir_cliente, name='excluir_cliente'),

    path('categorias/', views.lista_categorias, name='lista_categorias'),
    path('categorias/<int:categoria_id>/editar/', views.editar_categoria, name='editar_categoria'),
    path('categorias/<int:categoria_id>/excluir/', views.excluir_categoria, name='excluir_categoria'),

    path('cesta/', views.lista_cestas, name='lista_cestas'),
    path('cesta/<int:cesta_id>/editar/', views.editar_cesta, name='editar_cesta'),
    path('cesta/<int:cesta_id>/excluir/', views.excluir_cesta, name='excluir_cesta'),
]
