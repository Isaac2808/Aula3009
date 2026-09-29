from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages

from carrinho.models import Produto


def c_produto(request):

    if request.method == 'POST':

        try:

            nome = request.POST.get('nome')
            categoria = request.POST.get('categoria')
            preco = request.POST.get('preco')
            quantidade = request.POST.get('quantidade')
            descricao = request.POST.get('descricao')
            imagem = request.FILES.get('imagem')

            Produto.objects.create(
                nome=nome,
                categoria=categoria,
                preco=preco,
                quantidade=quantidade,
                descricao=descricao,
                imagem=imagem
            )

            messages.success(
                request,
                '✅ Produto cadastrado com sucesso!'
            )

            return redirect('c_produto')

        except Exception as erro:

            messages.error(
                request,
                f'❌ Erro ao cadastrar produto: {erro}'
            )

    produtos = Produto.objects.all().order_by('-id')

    return render(
        request,
        'c_produto.html',
        {
            'produtos': produtos
        }
    )


def remover_produto(request, id):

    produto = get_object_or_404(
        Produto,
        id=id
    )

    try:

        produto.delete()

        messages.success(
            request,
            '✅ Produto removido com sucesso!'
        )

    except Exception as erro:

        messages.error(
            request,
            f'❌ Erro ao remover produto: {erro}'
        )

    return redirect('c_produto')
