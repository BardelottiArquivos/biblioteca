# apps/reservas/admin.py
from django.contrib import admin
from .models import Reserva


@admin.register(Reserva)
class ReservaAdmin(admin.ModelAdmin):
    list_display = (
        'usuario', 'livro', 'status', 'posicao_fila',
        'data_reserva', 'notificado',
    )
    list_filter = ('status', 'notificado')
    search_fields = ('usuario__username', 'livro__titulo')
    date_hierarchy = 'data_reserva'
    actions = ['cancelar_reservas']

    @admin.action(description='Cancelar reservas selecionadas')
    def cancelar_reservas(self, request, queryset):
        atualizados = queryset.update(status='X')
        self.message_user(request, f'{atualizados} reserva(s) canceladas.')