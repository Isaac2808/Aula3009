from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.contrib import messages
from django.contrib.auth.models import User as Usuario, Group
from login.utils import verificar_grupo


@login_required(login_url='login')
def painel_principal(request):
    usuarios = {
        'usuarios': Usuario.objects.all()
    }
    return render(request, 'painel/home.html', usuarios)


@login_required
def view_administrador(request):
    if not verificar_grupo(request.user, 'administradores'):
        raise PermissionDenied
    return render(request, 'painel/administrador.html')


@login_required
def view_diretoria(request):
    if not verificar_grupo(request.user, 'diretoria'):
        raise PermissionDenied
    return render(request, 'painel/diretoria.html')


@login_required
def view_gerencia_geral(request):
    if not verificar_grupo(request.user, 'gerencia_geral'):
        raise PermissionDenied
    return render(request, 'painel/gerencia_geral.html')


@login_required
def view_gerencia(request):
    if not verificar_grupo(request.user, 'gerencia'):
        raise PermissionDenied
    return render(request, 'painel/gerencia.html')


# 🌸 Supervisão & Gestão de Usuários
@login_required
def view_supervisao(request):
    if not verificar_grupo(request.user, 'supervisao'):
        raise PermissionDenied

    context = {
        'usuarios': Usuario.objects.all().order_by('username'),
        'grupos': Group.objects.all()
    }
    return render(request, 'painel/supervisao.html', context)


@login_required
def editar_usuario_grupo(request, user_id):
    if not verificar_grupo(request.user, 'supervisao'):
        raise PermissionDenied

    if request.method == 'POST':
        usuario = get_object_or_404(Usuario, id=user_id)
        grupo_id = request.POST.get('grupo_id')

        usuario.groups.clear()
        if grupo_id:
            grupo = get_object_or_404(Group, id=grupo_id)
            usuario.groups.add(grupo)

        messages.success(request, f"Perfil do usuário {usuario.username} atualizado com sucesso!")

    return redirect('view_supervisao')


@login_required
def excluir_usuario(request, user_id):
    if not verificar_grupo(request.user, 'supervisao'):
        raise PermissionDenied

    usuario = get_object_or_404(Usuario, id=user_id)

    if usuario == request.user:
        messages.error(request, "Você não pode excluir seu próprio usuário!")
        return redirect('view_supervisao')

    usuario.delete()
    messages.success(request, "Usuário excluído com sucesso!")
    return redirect('view_supervisao')


@login_required
def view_atendente(request):
    if not verificar_grupo(request.user, 'atendente'):
        raise PermissionDenied
    return render(request, 'painel/atendente.html')


@login_required
def view_caixa(request):
    if not verificar_grupo(request.user, 'caixa'):
        raise PermissionDenied
    return render(request, 'painel/caixa.html')


# 🔧 Rotas internas do Caixa
@login_required
def registrar_recebimento(request):
    if not verificar_grupo(request.user, 'caixa'):
        raise PermissionDenied
    return render(request, 'painel/registrar_recebimento.html')


@login_required
def consultar_comprovantes(request):
    if not verificar_grupo(request.user, 'caixa'):
        raise PermissionDenied
    return render(request, 'painel/consultar_comprovantes.html')


@login_required
def pedidos_pagos(request):
    if not verificar_grupo(request.user, 'caixa'):
        raise PermissionDenied
    return render(request, 'painel/pedidos_pagos.html')


@login_required
def fechamento_diario(request):
    if not verificar_grupo(request.user, 'caixa'):
        raise PermissionDenied
    return render(request, 'painel/fechamento_diario.html')