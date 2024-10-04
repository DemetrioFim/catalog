from django.db import models
from django.utils import timezone

class Categoria(models.Model):
    nome = models.CharField(max_length=255)
    descricao = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.nome

class Produto(models.Model):
    nome = models.CharField(max_length=255)
    descricao = models.TextField()
    preco_venda = models.DecimalField(max_digits=10, decimal_places=2)
    preco_compra = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)  # Novo campo
    imagem = models.ImageField(upload_to='produtos/', blank=True, null=True)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, related_name='produtos')

    def __str__(self):
        return self.nome

class Cliente(models.Model):
    nome = models.CharField(max_length=255)
    email = models.EmailField(blank=True)
    telefone = models.CharField(max_length=15, blank=True, null=True)  # Telefone opcional
    endereco = models.TextField(blank=True, null=True)  # Endereço opcional

    def __str__(self):
        return self.nome

class Cesta(models.Model):
    STATUS_CHOICES = [
        ('pago', 'Pago'),
        ('pendente', 'Pendente'),
    ]

    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    criado_em = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pendente')

    def __str__(self):
        return f'Cesta {self.id} - {self.cliente.nome}'

class ItemCesta(models.Model):
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    cesta = models.ForeignKey(Cesta, on_delete=models.CASCADE)
    quantidade = models.PositiveIntegerField(default=1)
    preco_unitario = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, null=True, blank=True)  # Novo campo

    def __str__(self):
        return f'{self.quantidade}x {self.produto.nome}'

    @property
    def preco_total(self):
        return self.quantidade * self.preco_unitario  # Usando preco_unitario

class HistoricoPreco(models.Model):
    produto = models.ForeignKey(Produto, related_name='historico_precos', on_delete=models.CASCADE)
    preco_venda_antigo = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    preco_venda_novo = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    preco_compra_antigo = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    preco_compra_novo = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    alterado_em = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.produto.nome} - Alterado em {self.alterado_em}"
