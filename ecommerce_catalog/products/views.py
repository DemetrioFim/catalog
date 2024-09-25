# ecommerce_catalog/products/views.py

from django.shortcuts import render, redirect, get_object_or_404
from .models import Produto, Cesta, ItemCesta, ItemCesta, Cliente, Categoria
from .forms import ProdutoForm, ClienteForm, CategoriaForm, CestaComItensForm


def index(request):
    return render(request, 'products/index.html')


def lista_categorias(request):
    categorias = Categoria.objects.all()
    form = CategoriaForm()
    if request.method == 'POST':
        form = CategoriaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_categorias')

    return render(request, 'products/lista_categorias.html', {
        'categorias': categorias,
        'form': form
    })


def lista_produtos(request):
    produtos = Produto.objects.all()
    form = ProdutoForm()
    if request.method == 'POST':
        form = ProdutoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('lista_produtos')

    return render(request, 'products/lista_produtos.html', {
        'produtos': produtos,
        'form': form
    })


def lista_clientes(request):
    clientes = Cliente.objects.all()
    form = ClienteForm()
    if request.method == 'POST':
        form = ClienteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_clientes')

    return render(request, 'products/lista_clientes.html', {
        'clientes': clientes,
        'form': form
    })



def atualizar_item_cesta(request, item_id):
    item = get_object_or_404(ItemCesta, id=item_id)
    if request.method == 'POST':
        quantidade = request.POST.get('quantidade')
        if quantidade:
            item.quantidade = int(quantidade)
            item.save()
    return redirect('visualizar_cesta')


def adicionar_a_cesta(request, produto_id):
    produto = get_object_or_404(Produto, id=produto_id)
    cesta_id = request.session.get('cesta_id')
    if not cesta_id:
        cesta = Cesta.objects.create(cliente=None)  # Modifique conforme necessário
        request.session['cesta_id'] = cesta.id
    else:
        cesta = get_object_or_404(Cesta, id=cesta_id)

    item_cesta, created = ItemCesta.objects.get_or_create(cesta=cesta, produto=produto)
    if not created:
        item_cesta.quantidade += 1
    item_cesta.save()

    return redirect('lista_produtos')


def remover_item_cesta(request, produto_id):
    cesta_id = request.session.get('cesta_id')
    if not cesta_id:
        return redirect('lista_produtos')

    cesta = get_object_or_404(Cesta, id=cesta_id)
    item_cesta = get_object_or_404(ItemCesta, cesta=cesta, produto_id=produto_id)
    item_cesta.quantidade -= 1
    if item_cesta.quantidade <= 0:
        item_cesta.delete()
    else:
        item_cesta.save()

    return redirect('lista_produtos')


def cadastrar_produto(request):
    if request.method == 'POST':
        form = ProdutoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('lista_produtos')
    else:
        form = ProdutoForm()
    
    return render(request, 'products/cadastrar_produto.html', {'form': form})


def lista_cestas(request):
    # Ordena as cestas do maior para o menor pelo ID (ou use '-criado_em' para ordenar pela data de criação)
    cestas = Cesta.objects.all().order_by('-id')  # Ou substitua '-id' por '-criado_em' para data de criação

    # Filtros de cliente e status
    cliente_filtro = request.GET.get('cliente')
    status_filtro = request.GET.get('status')

    if cliente_filtro:
        cestas = cestas.filter(cliente_id=cliente_filtro)

    if status_filtro:
        cestas = cestas.filter(status=status_filtro)

    # Form para criar ou editar uma cesta
    if request.method == 'POST':
        form = CestaComItensForm(request.POST)
        if form.is_valid():
            cliente = form.cleaned_data['cliente']
            n_produtos = len([item for item in request.POST.keys() if item.startswith('produto_')])

            lista_produtos = []
            quantidades = []

            # Coletar produtos e quantidades
            for i in range(n_produtos):
                produto = int(request.POST.get(f'produto_{i}', 1))
                lista_produtos.append(produto)

            for i, produto_id in enumerate(lista_produtos):
                quantidade = int(request.POST.get(f'quantidade_{i}', 1))
                quantidades.append(quantidade)

            # Criação da cesta
            cesta = Cesta.objects.create(cliente=cliente)

            for produto_id, quantidade in zip(lista_produtos, quantidades):
                produto = Produto.objects.get(id=produto_id)
                ItemCesta.objects.create(cesta=cesta, produto=produto, quantidade=quantidade)

            return redirect('lista_cestas')
    else:
        form = CestaComItensForm()
        form.fields['produtos'].queryset = Produto.objects.all()

    # Calcular preços totais para cada cesta
    for cesta in cestas:
        cesta.preco_total = sum(item.preco_total for item in cesta.itemcesta_set.all())

    clientes = Cliente.objects.all()

    return render(request, 'products/lista_cestas.html', {
        'cestas': cestas,
        'form': form,
        'clientes': clientes,  # Passa a lista de clientes para o template
        'status_opcoes': Cesta.STATUS_CHOICES  # Passa as opções de status para o template
    })



def editar_cesta(request, cesta_id=None):
    if cesta_id:
        cesta = get_object_or_404(Cesta, id=cesta_id)
    else:
        cesta = None

    if request.method == 'POST':
        form = CestaComItensForm(request.POST)
        if form.is_valid():
            cliente = form.cleaned_data['cliente']
            status = form.cleaned_data['status']  # Certifique-se de pegar o status do form

            if cesta is None:
                # Cria a cesta se não existir
                cesta = Cesta.objects.create(cliente=cliente, status=status)
                print(f'Status salvo: {cesta.status}')  # Log para verificar o status salvo

            else:
                # Atualiza o status e cliente da cesta
                cesta.cliente = cliente
                cesta.status = status
                cesta.save()

                # Limpa os itens antigos para adicionar novos
                cesta.itemcesta_set.all().delete()

            # Adiciona os novos produtos à cesta
            n_produtos = len([item for item in request.POST.keys() if item.startswith('produto_')])
            lista_produtos = []
            quantidades = []

            for i in range(n_produtos):
                produto = int(request.POST.get(f'produto_{i}', 1))
                lista_produtos.append(produto)

            for i, produto_id in enumerate(lista_produtos):
                quantidade = int(request.POST.get(f'quantidade_{i}', 1))
                quantidades.append(quantidade)

            for produto_id, quantidade in zip(lista_produtos, quantidades):
                produto = Produto.objects.get(id=produto_id)
                ItemCesta.objects.create(cesta=cesta, produto=produto, quantidade=quantidade)

            return redirect('lista_cestas')
    else:
        initial_data = {'cliente': cesta.cliente.id, 'status': cesta.status} if cesta else {}
        form = CestaComItensForm(initial=initial_data)
        form.fields['produtos'].queryset = Produto.objects.all()

    return render(request, 'products/editar_cesta.html', {
        'form': form,
        'cesta': cesta,
    })


def cancelar_cesta(request):
    return redirect('lista_cestas')


def excluir_cesta(request, cesta_id):
    cesta = get_object_or_404(Cesta, id=cesta_id)
    cesta.delete()
    return redirect('lista_cestas')


# Editar Produto

def editar_produto(request, produto_id):
    produto = get_object_or_404(Produto, id=produto_id)
    if request.method == 'POST':
        form = ProdutoForm(request.POST, request.FILES, instance=produto)
        if form.is_valid():
            form.save()
            return redirect('lista_produtos')
    else:
        form = ProdutoForm(instance=produto)
    return render(request, 'products/editar_produto.html', {'form': form})

# Editar Cliente

def editar_cliente(request, cliente_id):
    cliente = get_object_or_404(Cliente, id=cliente_id)
    if request.method == 'POST':
        form = ClienteForm(request.POST, instance=cliente)
        if form.is_valid():
            form.save()
            return redirect('lista_clientes')
    else:
        form = ClienteForm(instance=cliente)
    return render(request, 'products/editar_cliente.html', {'form': form})

# Editar Categoria

def editar_categoria(request, categoria_id):
    categoria = get_object_or_404(Categoria, id=categoria_id)
    if request.method == 'POST':
        form = CategoriaForm(request.POST, instance=categoria)
        if form.is_valid():
            form.save()
            return redirect('lista_categorias')
    else:
        form = CategoriaForm(instance=categoria)
    return render(request, 'products/editar_categoria.html', {'form': form})

# Excluir Produto

def excluir_produto(request, produto_id):
    produto = get_object_or_404(Produto, id=produto_id)
    produto.delete()
    return redirect('lista_produtos')

# Excluir Cliente

def excluir_cliente(request, cliente_id):
    cliente = get_object_or_404(Cliente, id=cliente_id)
    cliente.delete()
    return redirect('lista_clientes')

# Excluir Categoria

def excluir_categoria(request, categoria_id):
    categoria = get_object_or_404(Categoria, id=categoria_id)
    categoria.delete()
    return redirect('lista_categorias')

def atualizar_preco_produto(request, produto_id):
    produto = get_object_or_404(Produto, id=produto_id)
    if request.method == 'POST':
        form = ProductPriceForm(request.POST)
        if form.is_valid():
            product_price = form.save(commit=False)
            product_price.produto = produto
            product_price.save()  # O sinal cuidará de atualizar o current_price e data_fim
            return redirect('lista_produtos')
    else:
        form = ProductPriceForm()
    
    return render(request, 'products/atualizar_preco_produto.html', {
        'form': form,
        'produto': produto,
    })


def lista_produtos(request):
    produtos = Produto.objects.all().select_related('categoria')
    return render(request, 'products/lista_produtos.html', {'produtos': produtos})
