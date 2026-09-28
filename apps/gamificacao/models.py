# apps/gamificacao/models.py
# ==============================================
# MODELOS DE GAMIFICAÇÃO
# ⚠️ CORRIGIDO: adicionado modelo Acao (faltava no original)
# ==============================================
from django.db import models
from django.contrib.auth.models import User


class Acao(models.Model):
    """
    Tipos de ações que geram pontos.
    ⚠️ MODELO FALTAVA NO DOCUMENTO ORIGINAL — foi adicionado aqui.
    """

    TIPO_CHOICES = [
        ('DOACAO', 'Doação de Livro'),
        ('EMPRESTIMO', 'Empréstimo Realizado'),
        ('DEVOLUCAO', 'Devolução no Prazo'),
        ('AVALIACAO', 'Avaliação de Livro'),
        ('CADASTRO', 'Cadastro na Plataforma'),
        ('CONVITE', 'Convite de Amigo'),
        ('LEITURA', 'Registro de Leitura'),
        ('RESENHA', 'Publicação de Resenha'),
    ]

    tipo = models.CharField(
        'Tipo', max_length=20, choices=TIPO_CHOICES, unique=True,
    )
    pontos = models.IntegerField('Pontos', default=0)
    descricao = models.CharField('Descrição', max_length=200, blank=True)
    icone = models.CharField('Ícone', max_length=10, blank=True)
    ativo = models.BooleanField('Ativo', default=True)

    class Meta:
        verbose_name = 'Ação'
        verbose_name_plural = 'Ações'
        ordering = ['tipo']

    def __str__(self):
        return f'{self.get_tipo_display()} ({self.pontos} pts)'


class PontuacaoUsuario(models.Model):
    """Pontuação acumulada por usuário."""

    usuario = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='pontuacao',
    )
    pontos_totais = models.IntegerField('Pontos Totais', default=0, db_index=True)
    nivel = models.IntegerField('Nível', default=1)
    titulo = models.CharField('Título', max_length=50, default='Novo Explorador')
    data_atualizacao = models.DateTimeField('Atualizado em', auto_now=True)

    class Meta:
        verbose_name = 'Pontuação'
        verbose_name_plural = 'Pontuações'
        ordering = ['-pontos_totais']

    def calcular_nivel(self):
        """Calcula nível baseado nos pontos totais."""
        if self.pontos_totais >= 1000:
            self.nivel, self.titulo = 5, 'Mestre Bibliotecário'
        elif self.pontos_totais >= 500:
            self.nivel, self.titulo = 4, 'Leitor Experiente'
        elif self.pontos_totais >= 200:
            self.nivel, self.titulo = 3, 'Leitor Ávido'
        elif self.pontos_totais >= 50:
            self.nivel, self.titulo = 2, 'Leitor Iniciante'
        else:
            self.nivel, self.titulo = 1, 'Novo Explorador'

        self.save(update_fields=['nivel', 'titulo'])
        return self.nivel

    def __str__(self):
        return f'{self.usuario.username} - {self.pontos_totais} pts (Nível {self.nivel})'


class HistoricoPontos(models.Model):
    """Histórico de todas as transações de pontos."""

    usuario = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='historico_pontos',
    )
    acao = models.ForeignKey(Acao, on_delete=models.PROTECT)
    pontos = models.IntegerField('Pontos')
    descricao = models.CharField('Descrição', max_length=300)
    data = models.DateTimeField('Data', auto_now_add=True)
    object_id = models.PositiveIntegerField('ID do Objeto', null=True, blank=True)
    content_type = models.CharField('Tipo de Objeto', max_length=50, blank=True)

    class Meta:
        verbose_name = 'Histórico de Pontos'
        verbose_name_plural = 'Históricos de Pontos'
        ordering = ['-data']

    def __str__(self):
        return f'{self.usuario.username} - {self.descricao} (+ {self.pontos} pts)'