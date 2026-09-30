from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from app import views as app_view
from cadastro import views as cadastro_view
from login import views as login_view
from painel import views as painel_views
from carrinho import views as carrinho_view
from c_produto import views as c_produto_view

urlpatterns = [
    # Administração
    path('admin/', admin.site.urls),

    # Home
    path('', app_view.home, name='home'),

    # Cadastro
    path('cadastro/', cadastro_view.cadastro, name='cadastro'),
    path('ativar/<uidb64>/<token>/', cadastro_view.ativar_conta, name='ativar_conta'),

    # Login
    path('login/', login_view.login_view, name='login'),
    path('login/mfa/', login_view.mfa_view, name='mfa'),
    path('logout/', login_view.logout_view, name='logout'),

    # Carrinho
    path('carrinho/', carrinho_view.ver_carrinho, name='ver_carrinho'),
    path('carrinho/checkout/', carrinho_view.checkout_view, name='checkout'),
    path('carrinho/finalizar/', carrinho_view.finalizar_compra_view, name='finalizar_compra'),
    path('carrinho/adicionar/<int:produto_id>/', carrinho_view.adicionar_carrinho, name='adicionar_carrinho'),
    path('carrinho/atualizar/', carrinho_view.atualizar_carrinho, name='atualizar_carrinho'),  # 🔄 nova rota
    path('carrinho/historico/', carrinho_view.historico_pedidos, name='historico_pedidos'),

    # Cadastro de Produto
    path('c_produto/', c_produto_view.c_produto, name='c_produto'),
    path('produto/remover/<int:id>/', c_produto_view.remover_produto, name='remover_produto'),
    path('produto/editar/<int:id>/', c_produto_view.editar_produto, name='editar_produto'),

    # Painel Principal
    path('painel/', login_view.painel_redirect, name='painel'),
    path('painel/home/', painel_views.painel_principal, name='painel_home'),

    # Painéis por grupo
    path('painel/administrador/', painel_views.view_administrador, name='view_administrador'),
    path('painel/diretoria/', painel_views.view_diretoria, name='view_diretoria'),
    path('painel/gerencia-geral/', painel_views.view_gerencia_geral, name='view_gerencia_geral'),
    path('painel/gerencia/', painel_views.view_gerencia, name='view_gerencia'),
    path('painel/supervisao/', painel_views.view_supervisao, name='view_supervisao'),
    path('painel/atendente/', painel_views.view_atendente, name='view_atendente'),
    path('painel/caixa/', painel_views.view_caixa, name='view_caixa'),

    # Rotas internas do Caixa
    path('painel/caixa/registrar-recebimento/', painel_views.registrar_recebimento, name='registrar_recebimento'),
    path('painel/caixa/comprovantes/', painel_views.consultar_comprovantes, name='consultar_comprovantes'),
    path('painel/caixa/pedidos-pagos/', painel_views.pedidos_pagos, name='pedidos_pagos'),
    path('painel/caixa/fechamento-diario/', painel_views.fechamento_diario, name='fechamento_diario'),
]

# Arquivos de mídia
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
