import json
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from .models import Pedido, PedidoItem, Produto


def ver_carrinho(request):
    """ Exibe os produtos adicionados ao carrinho """
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
    """
    Adiciona produto ao carrinho.
    Suporta chamadas AJAX (fetch) sem redirecionar a tela.
    """
    carrinho = request.session.get('carrinho', {})
    str_id = str(produto_id)
    carrinho[str_id] = carrinho.get(str_id, 0) + 1
    
    request.session['carrinho'] = carrinho
    request.session.modified = True

    carrinho_total = sum(carrinho.values())

    # Se a requisição veio via JS (fetch/AJAX)
    if request.headers.get('x-requested-with') == 'XMLHttpRequest' or request.method == 'POST':
        return JsonResponse({
            'sucesso': True,
            'carrinho_total': carrinho_total
        })

    messages.success(request, "Produto adicionado ao carrinho!")
    return redirect('ver_carrinho')


def atualizar_carrinho(request):
    """ Atualiza a quantidade dos itens via AJAX ou formulário """
    if request.method == 'POST':
        carrinho = request.session.get('carrinho', {})

        if request.content_type == 'application/json':
            dados = json.loads(request.body)
            produto_id = str(dados.get('produto_id'))
            qtd = int(dados.get('quantidade', 1))

            if produto_id in carrinho:
                if qtd > 0:
                    carrinho[produto_id] = qtd
                else:
                    carrinho.pop(produto_id, None)

            request.session['carrinho'] = carrinho
            request.session.modified = True

            subtotal_item = 0
            if produto_id in carrinho:
                try:
                    produto = Produto.objects.get(id=produto_id)
                    subtotal_item = produto.preco * carrinho[produto_id]
                except Produto.DoesNotExist:
                    pass

            total_geral = 0
            for p_id, q in carrinho.items():
                try:
                    prod = Produto.objects.get(id=p_id)
                    total_geral += prod.preco * q
                except Produto.DoesNotExist:
                    continue

            return JsonResponse({
                'sucesso': True,
                'subtotal': f"{subtotal_item:.2f}",
                'total': f"{total_geral:.2f}",
                'carrinho_total': sum(carrinho.values())
            })

        # Fallback tradicional
        for produto_id in list(carrinho.keys()):
            qtd = request.POST.get(f'quantidade_{produto_id}')
            if qtd:
                try:
                    carrinho[produto_id] = max(1, int(qtd))
                except ValueError:
                    continue
        request.session['carrinho'] = carrinho
        request.session.modified = True
        messages.success(request, "Carrinho atualizado com sucesso!")

    return redirect('ver_carrinho')


def checkout_view(request):
    """
    Tela de Checkout:
    1. Se o usuário NÃO estiver logado: exibe os botões para fazer Login ou Cadastrar.
    2. Se estiver logado: exibe os campos para preencher Endereço e Pagamento.
    """
    carrinho = request.session.get('carrinho', {})
    if not carrinho:
        messages.error(request, "Seu carrinho está vazio.")
        return redirect('ver_carrinho')

    # Se o formulário de Endereço/Pagamento for enviado (POST)
    if request.method == 'POST' and request.user.is_authenticated:
        endereco = request.POST.get('endereco')
        pagamento = request.POST.get('pagamento')

        if not endereco or not pagamento:
            messages.error(request, "Por favor, preencha todos os campos antes de continuar.")
            return redirect('checkout')

        # Salva as informações na sessão
        request.session['checkout_data'] = {
            'endereco': endereco,
            'pagamento': pagamento,
        }
        request.session.modified = True
        return redirect('finalizar_compra')

    return render(request, 'checkout.html')


@login_required(login_url='checkout')
def finalizar_compra_view(request):
    """
    Tela de Revisão Final:
    Exibe os itens e os dados salvos de entrega/pagamento.
    Ao clicar em "Confirmar e Concluir Pedido", grava no banco e volta para a Home.
    """
    carrinho = request.session.get('carrinho', {})
    checkout_data = request.session.get('checkout_data')

    # Se faltar o carrinho ou os dados de entrega, volta para o checkout
    if not carrinho or not checkout_data:
        messages.error(request, "Por favor, informe o endereço e a forma de pagamento.")
        return redirect('checkout')

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

    # Confirmação Final do Pedido (POST da tela de resumo)
    if request.method == 'POST':
        pedido = Pedido.objects.create(
            usuario=request.user,
            endereco=checkout_data['endereco'],
            pagamento=checkout_data['pagamento']
        )

        for item in itens:
            PedidoItem.objects.create(
                pedido=pedido,
                produto=item['produto'],
                quantidade=item['quantidade'],
                preco_unitario=item['produto'].preco
            )

        # Limpa o carrinho e os dados da sessão
        request.session.pop('carrinho', None)
        request.session.pop('checkout_data', None)
        request.session.modified = True

        messages.success(request, "Compra realizada com sucesso! Obrigado por comprar na Ponto de Flor. 🌸")
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