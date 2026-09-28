# apps/emprestimos/admin.py
from django.contrib import admin
from django.utils import timezone
from .models import SolicitacaoEmprestimo


@admin.register(SolicitacaoEmprestimo)
class SolicitacaoEmprestimoAdmin(admin.ModelAdmin):
    list_display = ('solicitante', 'livro', 'status', 'data_solicitacao', 'data_aprovacao')
    list_filter = ('status',)
    search_fields = ('solicitante__username', 'livro__titulo')
    date_hierarchy = 'data_solicitacao'
    readonly_fields = ('data_solicitacao',)
    actions = ['aprovar_solicitacoes', 'marcar_devolvido']

    @admin.action(description='Aprovar solicitações selecionadas')
    def aprovar_solicitacoes(self, request, queryset):
        atualizados = queryset.filter(status='P').update(
            status='A', data_aprovacao=timezone.now(),
        )
        self.message_user(request, f'{atualizados} solicitação(ões) aprovadas.')

    @admin.action(description='Marcar como devolvido')
    def marcar_devolvido(self, request, queryset):
        atualizados = queryset.filter(status='A').update(
            status='D', data_devolucao=timezone.now(),
        )
        self.message_user(request, f'{atualizados} empréstimo(s) marcados como devolvidos.')