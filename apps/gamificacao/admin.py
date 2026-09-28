# apps/gamificacao/admin.py
from django.contrib import admin
from .models import Acao, PontuacaoUsuario, HistoricoPontos


@admin.register(Acao)
class AcaoAdmin(admin.ModelAdmin):
    list_display = ('icone', 'tipo', 'pontos', 'descricao', 'ativo')
    list_filter = ('ativo',)
    list_editable = ('pontos', 'ativo')


@admin.register(PontuacaoUsuario)
class PontuacaoUsuarioAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'pontos_totais', 'nivel', 'titulo', 'data_atualizacao')
    list_filter = ('nivel',)
    search_fields = ('usuario__username',)
    actions = ['recalcular_niveis']

    @admin.action(description='Recalcular níveis')
    def recalcular_niveis(self, request, queryset):
        for p in queryset:
            p.calcular_nivel()
        self.message_user(request, f'{queryset.count()} pontuação(ões) recalculadas.')


@admin.register(HistoricoPontos)
class HistoricoPontosAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'acao', 'pontos', 'descricao', 'data')
    list_filter = ('acao',)
    search_fields = ('usuario__username', 'descricao')
    date_hierarchy = 'data'