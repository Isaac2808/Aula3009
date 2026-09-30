from django.shortcuts import render
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

