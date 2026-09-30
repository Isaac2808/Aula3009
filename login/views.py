from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied

# Limita o acesso a usuários autenticados e verifica se pertencem a um grupo específico.
from login.utils import verificar_grupo

# Limita a view aos métodos HTTP usados pelo formulário de login.
from django.views.decorators.http import require_http_methods

# Recursos necessários para enviar o código MFA por e-mail.
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from .models import TwoFactorCode


@require_http_methods(["GET", "POST"])
def login_view(request):
    """Valida a senha e inicia a segunda etapa da autenticação."""
    if request.method == 'POST':
        email = request.POST.get('email')
        senha = request.POST.get('senha')

        usuario_objeto = User.objects.filter(email=email).first()

        if usuario_objeto:
            user = authenticate(request, username=usuario_objeto.username, password=senha)

            if user is not None:
                # Invalida códigos anteriores não usados
                TwoFactorCode.objects.filter(user=user, is_used=False).update(is_used=True)

                # Cria novo código MFA
                two_factor_obj = TwoFactorCode.objects.create(user=user)

                domain = get_current_site(request).domain

                send_mail(
                    subject=f'Seu código de autenticação no site {domain}',
                    message=f'Seu código de acesso de 6 dígitos é: {two_factor_obj.code}. Ele é válido por 5 minutos.',
                    from_email=f'no-reply@{domain}',
                    recipient_list=[user.email],
                    fail_silently=False,
                )

                # Guarda ID do usuário para segunda etapa
                request.session['pre_2fa_user_id'] = user.id
                return redirect('mfa')

            # Caso a conta não esteja ativada
            if not usuario_objeto.is_active and usuario_objeto.check_password(senha):
                messages.error(request, "Sua conta ainda não foi ativada. Verifique seu e-mail.")
                return render(request, "login/login.html")

        messages.error(request, "E-mail ou senha inválidos.")

    return render(request, 'login/login.html')


def mfa_view(request):
    """Valida o código MFA e efetiva o login após a senha ser aceita."""
    user_id = request.session.get('pre_2fa_user_id')

    if not user_id:
        return redirect('login')

    if request.method == 'POST':
        code_input = request.POST.get('code')

        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return redirect('login')

        two_factor_obj = TwoFactorCode.objects.filter(
            user=user,
            code=code_input,
            is_used=False
        ).order_by('-created_at').first()

        if two_factor_obj and two_factor_obj.is_valid():
            two_factor_obj.mark_as_used()
            login(request, user)

            # Remove chaves temporárias de forma segura
            request.session.pop('pre_2fa_user_id', None)
            request.session.pop('mfa_code', None)

            return redirect('painel')
        else:
            messages.error(request, 'Código inválido ou expirado.')

    return render(request, 'login/mfa.html')


def logout_view(request):
    """Encerra a sessão atual e volta para a página inicial."""
    logout(request)
    return redirect('home')


@login_required
def painel_redirect(request):
    """Redireciona para o painel correto de acordo com o grupo do usuário."""
    user = request.user

    if verificar_grupo(user, 'administradores'):
        return redirect('view_administrador')
    elif verificar_grupo(user, 'diretoria'):
        return redirect('view_diretoria')
    elif verificar_grupo(user, 'gerencia_geral'):
        return redirect('view_gerencia_geral')
    elif verificar_grupo(user, 'gerencia'):
        return redirect('view_gerencia')
    elif verificar_grupo(user, 'supervisao'):
        return redirect('view_supervisao')
    elif verificar_grupo(user, 'atendente'):
        return redirect('view_atendente')
    elif verificar_grupo(user, 'caixa'):
        return redirect('view_caixa')

    # Em vez de interromper com erro 403 (PermissionDenied), 
    # redireciona os clientes e novos usuários para a loja/Home
    return redirect('home')
