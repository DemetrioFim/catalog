from django.db import models

class Categoria(models.Model):
    nome = models.CharField(max_length=255)
    descricao = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.nome

class Produto(models.Model):
    nome = models.CharField(max_length=255)
    descricao = models.TextField()
    preco = models.DecimalField(max_digits=10, decimal_places=2)
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

    def __str__(self):
        return f'{self.quantidade}x {self.produto.nome}'

    @property
    def preco_total(self):
        return self.quantidade * self.produto.preco


