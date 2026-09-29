from django.shortcuts import render
from carrinho.models import Produto

def home(request):

    produtos = Produto.objects.all()

    return render(
        request,
        'app/index.html',
        {
            'produtos': produtos
        }
    )