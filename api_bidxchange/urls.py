from django.contrib import admin
from django.urls import path

from . import views

urlpatterns = [
    path('conta/registrar/', views.criar_conta, name='criar_conta'), # testado
    path('conta/login/', views.login_conta, name='login_conta'), # testado
    path('conta/modificar/', views.modificar_conta, name='modificar_conta'), # testado
    path('cotacao/criar/', views.criar_cotacao, name='criar_cotacao'), # testado
    path('cotacao/listar/', views.listar_cotacoes, name='listar_cotacoes'), # testado
    path('cotacao/<int:id>/', views.cotacao_id, name='cotacao_id'), # testado
    path('cotacao/encerrar/<int:id>/', views.encerrar_cotacao, name='encerrar_cotacao'), # testado
    path('conta/', views.conta, name='conta'), # testado
    path('favorito/criar/<int:id>/<str:categoria>/<int:nota>/', views.adicionar_favorito, name='adicionar_favorito'), # testado
    path('favorito/verFavoritos/', views.ver_favoritos, name='ver_favoritos'), # testado
    path('conta/verTodasAsMensagens/', views.ver_todos_os_usuarios_mensagens, name='ver_todos_os_usuarios_mensagens'), # testado
    path('conta/verMensagensUsuario/<int:id>/', views.ver_mensagens_usuario, name='ver_mensagens_usuario'),  # testado
    path('conta/enviarMensagem/<int:id_usuario_destinatario>/', views.enviar_mensagem, name='enviar_mensagem'), # testado
    path('conta/criarProposta/', views.criar_proposta, name='criar_proposta'), # testado
    path('conta/verPropostas/', views.ver_propostas, name='ver_propostas'), # testado
    path('conta/verPropostaId/<int:id>/', views.ver_proposta_id, name='ver_proposta_id'), # testado
    path('conta/enviarConvite/', views.enviar_convite, name='enviar_convite'),
    path('conta/verConvites/', views.ver_convites, name='ver_convites'), # testado
    path('conta/deletarConvite/<int:id>/', views.deletar_convite, name='deletar_convite'), # testado
    path('conta/suporteEnviarEmail/', views.enviar_mensagem_suporte, name='enviar_mensagem_suporte'), # testado
    path('conta/esqueciSenha/enviarEmail/', views.enviar_email_senha, name='enviar_email_senha'), # testado
    path('conta/esqueciSenha/mudarSenha/', views.mudar_senha, name='mudar_senha'), # testado
]
