from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from carrinho.models import Produto

def home(request):
    produtos = Produto.objects.all()
    carrinho = request.session.get('carrinho', {})
    carrinho_total = sum(carrinho.values())  # soma todas as quantidades

    return render(
        request,
        'app/index.html',
        {
            'produtos': produtos,
            'carrinho_total': carrinho_total
        }
    )


def adicionar_carrinho(request, produto_id):
    # Recupera o dicionário do carrinho na sessão (ou cria um novo se não existir)
    carrinho = request.session.get('carrinho', {})
    
    # Converte o ID para string pois chaves de dicionários da sessão do Django são serializadas como string
    str_produto_id = str(produto_id)
    
    # Incrementa a quantidade do produto no carrinho
    carrinho[str_produto_id] = carrinho.get(str_produto_id, 0) + 1
    
    # Salva o carrinho de volta na sessão
    request.session['carrinho'] = carrinho
    request.session.modified = True
    
    # Calcula o novo total acumulado
    carrinho_total = sum(carrinho.values())

    # Se a requisição veio do JavaScript (Fetch / AJAX)
    if request.headers.get('x-requested-with') == 'XMLHttpRequest' or request.method == 'POST':
        return JsonResponse({
            'status': 'sucesso',
            'carrinho_total': carrinho_total
        })

    # Fallback: se o usuário acessar o link direto pelo navegador sem JS, redireciona de volta
    return redirect('home')