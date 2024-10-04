# admin.py

from django.contrib import admin
from .models import Produto, HistoricoPreco

class HistoricoPrecoInline(admin.TabularInline):
    model = HistoricoPreco
    readonly_fields = ('preco_venda_antigo', 'preco_venda_novo', 'preco_compra_antigo', 'preco_compra_novo', 'alterado_em')
    can_delete = False
    extra = 0

@admin.register(Produto)
class ProdutoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'preco_venda', 'preco_compra', 'categoria')
    inlines = [HistoricoPrecoInline]

@admin.register(HistoricoPreco)
class HistoricoPrecoAdmin(admin.ModelAdmin):
    list_display = ('produto', 'alterado_em')
    readonly_fields = ('produto', 'preco_venda_antigo', 'preco_venda_novo', 'preco_compra_antigo', 'preco_compra_novo', 'alterado_em')
