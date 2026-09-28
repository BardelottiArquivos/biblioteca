# apps/acervo/admin.py
from django.contrib import admin
from django.utils.html import format_html
from .models import Livro, Avaliacao


@admin.register(Livro)
class LivroAdmin(admin.ModelAdmin):
    list_display = (
        'titulo', 'autor', 'genero', 'status_badge',
        'tipo_midia', 'acessibilidade_badge', 'doador', 'data_cadastro',
    )
    list_filter = ('status', 'genero', 'tipo_midia', 'possui_braille', 'possui_audio')
    search_fields = ('titulo', 'autor', 'isbn')
    prepopulated_fields = {'slug': ('titulo',)}
    readonly_fields = ('data_cadastro', 'atualizado_em', 'criado_em', 'qr_code')
    date_hierarchy = 'data_cadastro'
    actions = ['marcar_disponivel_emprestimo', 'marcar_indisponivel', 'gerar_qrcodes']

    @admin.display(description='Status')
    def status_badge(self, obj):
        cores = {
            'DD': '#28a745', 'DE': '#17a2b8', 'RE': '#ffc107',
            'EM': '#fd7e14', 'IN': '#dc3545',
        }
        cor = cores.get(obj.status, '#6c757d')
        return format_html(
            '<span style="background:{};color:#fff;padding:3px 8px;'
            'border-radius:4px;">{}</span>',
            cor, obj.get_status_display(),
        )

    @admin.display(description='Acessibilidade')
    def acessibilidade_badge(self, obj):
        recursos = obj.recursos_acessibilidade
        return ', '.join(recursos) if recursos else '-'

    @admin.action(description='Marcar como disponível para empréstimo')
    def marcar_disponivel_emprestimo(self, request, queryset):
        atualizados = queryset.update(status='DE')
        self.message_user(request, f'{atualizados} livro(s) marcados como disponíveis.')

    @admin.action(description='Marcar como indisponível')
    def marcar_indisponivel(self, request, queryset):
        atualizados = queryset.update(status='IN')
        self.message_user(request, f'{atualizados} livro(s) marcados como indisponíveis.')

    @admin.action(description='Gerar QR Codes em massa')
    def gerar_qrcodes(self, request, queryset):
        try:
            from apps.qrcode.services import QRCodeGenerator
            resultados = QRCodeGenerator.gerar_qr_code_massa(queryset)
            sucessos = sum(1 for r in resultados if r.get('sucesso'))
            self.message_user(request, f'{sucessos} QR Code(s) gerados.')
        except Exception as e:
            self.message_user(request, f'Erro: {e}', level='error')


@admin.register(Avaliacao)
class AvaliacaoAdmin(admin.ModelAdmin):
    list_display = ('livro', 'usuario', 'nota', 'data_avaliacao')
    list_filter = ('nota',)
    search_fields = ('livro__titulo', 'usuario__username')
    date_hierarchy = 'data_avaliacao'