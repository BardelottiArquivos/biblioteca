# apps/notificacoes/services.py
# ==============================================
# SERVIÇO DE NOTIFICAÇÕES
# ==============================================
import logging
from django.core.mail import send_mail
from django.conf import settings

logger = logging.getLogger(__name__)


class NotificacaoService:
    """Serviço para envio de notificações (email e push)."""

    @staticmethod
    def enviar_notificacao(usuario, tipo, titulo, mensagem, link=None):
        """Envia notificação para um usuário."""
        try:
            if usuario.email:
                NotificacaoService._enviar_email(
                    usuario=usuario, titulo=titulo, mensagem=mensagem, link=link,
                )
            logger.info(f'Notificação enviada para {usuario.username}: {titulo}')
            return True
        except Exception as e:
            logger.error(f'Erro ao enviar notificação: {str(e)}')
            return False

    @staticmethod
    def _enviar_email(usuario, titulo, mensagem, link=None):
        """Envia email para o usuário."""
        try:
            link_html = ''
            if link:
                link_html = (
                    f'<a href="{link}" style="display:inline-block;'
                    f'background:#2c6b8f;color:#fff;padding:10px 20px;'
                    f'text-decoration:none;border-radius:5px;">Acessar agora</a>'
                )

            corpo_html = f"""
            <html>
            <body style="font-family: Arial, sans-serif; color: #333;">
                <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
                    <h2 style="color: #2c6b8f;">{titulo}</h2>
                    <p>{mensagem}</p>
                    <div style="text-align: center; margin: 20px 0;">{link_html}</div>
                    <hr>
                    <div style="text-align: center; padding: 20px;
                                font-size: 12px; color: #999;">
                        <p>Este é um e-mail automático. Por favor, não responda.</p>
                    </div>
                </div>
            </body>
            </html>
            """

            send_mail(
                subject=titulo,
                message=mensagem,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[usuario.email],
                html_message=corpo_html,
                fail_silently=False,
            )
            return True
        except Exception as e:
            logger.error(f'Erro ao enviar email: {str(e)}')
            return False