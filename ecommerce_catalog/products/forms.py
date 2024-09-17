from django import forms
from .models import Cesta, ItemCesta, Produto, Cliente, Categoria

class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = ['nome', 'descricao']

class ProdutoForm(forms.ModelForm):
    class Meta:
        model = Produto
        fields = ['nome', 'descricao', 'preco', 'imagem', 'categoria']  # Inclui o campo de categoria

class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['nome', 'email', 'telefone', 'endereco']

class CestaForm(forms.ModelForm):
    class Meta:
        model = Cesta
        fields = ['cliente']

class ItemCestaForm(forms.ModelForm):
    class Meta:
        model = ItemCesta
        fields = ['produto', 'quantidade']

class CestaComItensForm(forms.Form):
    cliente = forms.ModelChoiceField(queryset=Cliente.objects.all(), label="Cliente")
    produtos = forms.ModelChoiceField(queryset=Produto.objects.all(), label="Produto", required=False)
    status = forms.ChoiceField(choices=Cesta.STATUS_CHOICES, label="Status")

