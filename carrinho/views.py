from django.shortcuts import render


def ver_carrinho(request):
    return render(
        request,
        'carrinho.html'
    )


def c_produto(request):
    return render(
        request,
        'c_produto.html'
    )
# Create your views here.
