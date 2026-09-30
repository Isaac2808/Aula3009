from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Pedido, PedidoItem, Produto


def ver_carrinho(request):
    carrinho = request.session.get('carrinho', {})
    itens = []
    total = 0

    for produto_id, qtd in carrinho.items():
        try:
            produto = Produto.objects.get(id=produto_id)
            subtotal = produto.preco * qtd
            itens.append({
                'produto': produto,
                'quantidade': qtd,
                'subtotal': subtotal
            })
            total += subtotal
        except Produto.DoesNotExist:
            continue

    return render(request, 'carrinho.html', {
        'itens': itens,
        'total': total
    })


def adicionar_carrinho(request, produto_id):
    carrinho = request.session.get('carrinho', {})
    carrinho[str(produto_id)] = carrinho.get(str(produto_id), 0) + 1
    request.session['carrinho'] = carrinho
    messages.success(request, "Produto adicionado ao carrinho!")
    return redirect('ver_carrinho')


def atualizar_carrinho(request):
    if request.method == 'POST':
        carrinho = request.session.get('carrinho', {})
        for produto_id in list(carrinho.keys()):
            qtd = request.POST.get(f'quantidade_{produto_id}')
            if qtd:
                try:
                    carrinho[produto_id] = max(1, int(qtd))  # garante mínimo 1
                except ValueError:
                    continue
        request.session['carrinho'] = carrinho
        messages.success(request, "Carrinho atualizado com sucesso!")
    return redirect('ver_carrinho')


@login_required
def checkout_view(request):
    carrinho = request.session.get('carrinho', {})
    if not carrinho:
        messages.error(request, "Seu carrinho está vazio.")
        return redirect('ver_carrinho')

    itens = []
    total = 0
    for produto_id, qtd in carrinho.items():
        try:
            produto = Produto.objects.get(id=produto_id)
            subtotal = produto.preco * qtd
            itens.append({
                'produto': produto,
                'quantidade': qtd,
                'subtotal': subtotal
            })
            total += subtotal
        except Produto.DoesNotExist:
            continue

    if request.method == 'POST':
        endereco = request.POST.get('endereco')
        pagamento = request.POST.get('pagamento')

        # ✅ Validação dos campos obrigatórios
        if not endereco or not pagamento:
            messages.error(request, "Por favor, preencha todos os campos antes de continuar.")
            return redirect('checkout')

        request.session['checkout_data'] = {
            'endereco': endereco,
            'pagamento': pagamento,
        }
        return redirect('finalizar_compra')

    return render(request, 'checkout.html', {
        'itens': itens,
        'total': total
    })


@login_required
def finalizar_compra_view(request):
    carrinho = request.session.get('carrinho', {})
    checkout_data = request.session.get('checkout_data')

    if not carrinho or not checkout_data:
        return redirect('ver_carrinho')

    itens = []
    total = 0
    for produto_id, qtd in carrinho.items():
        try:
            produto = Produto.objects.get(id=produto_id)
            subtotal = produto.preco * qtd
            itens.append({
                'produto': produto,
                'quantidade': qtd,
                'subtotal': subtotal
            })
            total += subtotal
        except Produto.DoesNotExist:
            continue

    if request.method == 'POST':
        pedido = Pedido.objects.create(
            usuario=request.user,
            endereco=checkout_data['endereco'],
            pagamento=checkout_data['pagamento']
        )

        for produto_id, qtd in carrinho.items():
            try:
                produto = Produto.objects.get(id=produto_id)
                PedidoItem.objects.create(
                    pedido=pedido,
                    produto=produto,
                    quantidade=qtd,
                    preco_unitario=produto.preco  # ✅ salva o preço atual do produto
                )
            except Produto.DoesNotExist:
                messages.error(request, f"Produto {produto_id} não encontrado.")

        request.session.pop('carrinho', None)
        request.session.pop('checkout_data', None)

        messages.success(request, "Compra concluída com sucesso!")
        return redirect('home')

    return render(request, 'finalizar.html', {
        'itens': itens,
        'total': total,
        'checkout': checkout_data
    })

@login_required
def historico_pedidos(request):
    pedidos = Pedido.objects.filter(usuario=request.user).order_by('-data')
    return render(request, 'historico.html', {
        'pedidos': pedidos
    })


# Create your views here.
