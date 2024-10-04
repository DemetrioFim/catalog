# signals.py

from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils import timezone
from .models import Produto, HistoricoPreco

@receiver(pre_save, sender=Produto)
def salvar_historico_preco(sender, instance, **kwargs):
    if not instance.pk:
        # Produto novo, não precisa registrar histórico
        return

    try:
        produto_antigo = Produto.objects.get(pk=instance.pk)
    except Produto.DoesNotExist:
        return

    preco_venda_alterado = produto_antigo.preco_venda != instance.preco_venda
    preco_compra_alterado = produto_antigo.preco_compra != instance.preco_compra

    if preco_venda_alterado or preco_compra_alterado:
        HistoricoPreco.objects.create(
            produto=instance,
            preco_venda_antigo=produto_antigo.preco_venda if preco_venda_alterado else None,
            preco_venda_novo=instance.preco_venda if preco_venda_alterado else None,
            preco_compra_antigo=produto_antigo.preco_compra if preco_compra_alterado else None,
            preco_compra_novo=instance.preco_compra if preco_compra_alterado else None,
            alterado_em=timezone.now()
        )
