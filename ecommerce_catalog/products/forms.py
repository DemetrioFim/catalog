from django import forms
from .models import Cesta, ItemCesta, Produto, Cliente, Categoria

class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = ['nome', 'descricao']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control'}),
            'descricao': forms.Textarea(attrs={'class': 'form-control'}),
        }

class ProdutoForm(forms.ModelForm):
    class Meta:
        model = Produto
        fields = ['nome', 'descricao', 'preco_venda', 'preco_compra', 'imagem', 'categoria']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control'}),
            'descricao': forms.Textarea(attrs={'class': 'form-control'}),
            'preco_venda': forms.NumberInput(attrs={'class': 'form-control'}),
            'preco_compra': forms.NumberInput(attrs={'class': 'form-control'}),
            'categoria': forms.Select(attrs={'class': 'form-control'}),
            'imagem': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
        }

class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['nome', 'email', 'telefone', 'endereco']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'telefone': forms.NumberInput(attrs={'class': 'form-control'}),
            'endereco': forms.Textarea(attrs={'class': 'form-control'}),
        }

class CestaForm(forms.ModelForm):
    class Meta:
        model = Cesta
        fields = ['cliente']
        # widgets = {'cliente': forms.TextInput(attrs={'class': 'form-control'}),}

class ItemCestaForm(forms.ModelForm):
    class Meta:
        model = ItemCesta
        fields = ['produto', 'quantidade']
        widgets = {
            'produto': forms.Select(attrs={'class': 'form-control'}),
            'quantidade': forms.NumberInput(attrs={'class': 'form-control'}),
        }

class CestaComItensForm(forms.Form):
    cliente = forms.ModelChoiceField(queryset=Cliente.objects.all(), label="Cliente")
    produtos = forms.ModelChoiceField(queryset=Produto.objects.all(), label="Produto", required=False)
    status = forms.ChoiceField(choices=Cesta.STATUS_CHOICES, label="Status")
    # widgets = {
    #     'cliente': forms.TextInput(attrs={'class': 'form-control'}),
    #     'produtos': forms.NumberInput(attrs={'class': 'form-control'}),
    #     'status': forms.Select(attrs={'class': 'form-control'}),
    # }

