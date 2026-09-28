# apps/chat/consumers.py
# ==============================================
# CONSUMER DE CHAT EM TEMPO REAL
# ==============================================
import json

from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async


class ChatConsumer(AsyncWebsocketConsumer):
    """Gerencia conexões WebSocket para chat em tempo real."""

    async def connect(self):
        self.conversa_id = self.scope['url_route']['kwargs']['conversa_id']
        self.room_group_name = f'chat_{self.conversa_id}'

        user = self.scope['user']
        if not user.is_authenticated:
            await self.close()
            return

        if not await self._usuario_na_conversa(user, self.conversa_id):
            await self.close()
            return

        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        if hasattr(self, 'room_group_name'):
            await self.channel_layer.group_discard(
                self.room_group_name, self.channel_name,
            )

    async def receive(self, text_data):
        data = json.loads(text_data)
        mensagem = data.get('mensagem', '').strip()

        if not mensagem:
            return

        mensagem_obj = await self._salvar_mensagem(
            self.scope['user'], self.conversa_id, mensagem,
        )

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',  # CORRIGIDO: era 'type' com aspas malformadas
                'mensagem': mensagem,
                'remetente': self.scope['user'].username,
                'data_envio': str(mensagem_obj.data_envio),
                'id': mensagem_obj.id,
            },
        )

    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            'mensagem': event['mensagem'],
            'remetente': event['remetente'],
            'data_envio': event['data_envio'],
            'id': event['id'],
        }))

    @database_sync_to_async
    def _usuario_na_conversa(self, user, conversa_id):
        from .models import Conversa
        return Conversa.objects.filter(
            id=conversa_id, participantes=user
        ).exists()

    @database_sync_to_async
    def _salvar_mensagem(self, user, conversa_id, conteudo):
        from .models import Conversa, Mensagem
        conversa = Conversa.objects.get(id=conversa_id)
        mensagem = Mensagem.objects.create(
            conversa=conversa, remetente=user, conteudo=conteudo,
        )
        conversa.data_atualizacao = mensagem.data_envio
        conversa.save(update_fields=['data_atualizacao'])
        return mensagem