# apps/chat/admin.py
from django.contrib import admin
from .models import Conversa, Mensagem


@admin.register(Conversa)
class ConversaAdmin(admin.ModelAdmin):
    list_display = ('id', 'livro', 'data_atualizacao')
    filter_horizontal = ('participantes',)


@admin.register(Mensagem)
class MensagemAdmin(admin.ModelAdmin):
    list_display = ('remetente', 'conversa', 'data_envio', 'lida')
    list_filter = ('lida',)