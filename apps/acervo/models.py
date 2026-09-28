# apps/acervo/models.py
# ===========================================
# MODELOS DE ACERVO - LIVROS E AVALIAÇÕES
# ===========================================
import re
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone

from apps.core.models import BaseModel, AddressMixin
from apps.core.validators import SecurityValidator
from apps.core.utils import generate_slug


class GeneroLiterario(models.TextChoices):
    FICCAO = 'FIC', 'Ficção'
    NAO_FICCAO = 'NAO', 'Não-ficção'
    ROMANCE = 'ROM', 'Romance'
    FANTASIA = 'FAN', 'Fantasia'
    FICCAO_CIENTIFICA = 'FIC_CI', 'Ficção Científica'
    MISTERIO = 'MIS', 'Mistério'
    SUSPENSE = 'SUS', 'Suspense'
    TERROR = 'TER', 'Terror'
    AVENTURA = 'AVE', 'Aventura'
    POESIA = 'POE', 'Poesia'
    DRAMA = 'DRA', 'Drama'
    BIOGRAFIA = 'BIO', 'Biografia'
    AUTOBIOGRAFIA = 'AUT', 'Autobiografia'
    HISTORIA = 'HIS', 'História'
    CIENCIA = 'CIE', 'Ciência'
    TECNOLOGIA = 'TEC', 'Tecnologia'
    FILOSOFIA = 'FIL', 'Filosofia'
    RELIGIAO = 'REL', 'Religião'
    AUTO_AJUDA = 'AAJ', 'Auto-ajuda'
    DESENVOLVIMENTO_PESSOAL = 'DEP', 'Desenvolvimento Pessoal'
    EDUCACAO = 'EDU', 'Educação'
    PSICOLOGIA = 'PSI', 'Psicologia'
    SAUDE = 'SAU', 'Saúde'
    INFANTIL = 'INF', 'Infantil'
    JUVENIL = 'JUV', 'Juvenil'
    HQS = 'HQS', 'HQs e Mangás'
    OUTROS = 'OUT', 'Outros'


class StatusLivro(models.TextChoices):
    DISPONIVEL_DOACAO = 'DD', 'Disponível para Doação'
    DISPONIVEL_EMPRESTIMO = 'DE', 'Disponível para Empréstimo'
    RESERVADO = 'RE', 'Reservado'
    EMPRESTADO = 'EM', 'Emprestado'
    INDISPONIVEL = 'IN', 'Indisponível'


class TipoMidia(models.TextChoices):
    FISICO = 'FI', 'Físico'
    DIGITAL = 'DI', 'Digital'
    AUDIOLIVRO = 'AU', 'Audiolivro'
    EBOOK = 'EB', 'E-book'


class Livro(BaseModel, AddressMixin):
    """Modelo principal de Livro."""

    # ===========================================
    # METADADOS
    # ===========================================
    titulo = models.CharField('Título', max_length=200, db_index=True)
    subtitulo = models.CharField('Subtítulo', max_length=200, blank=True)
    autor = models.CharField('Autor', max_length=200, db_index=True)
    isbn = models.CharField('ISBN', max_length=17, blank=True, db_index=True)
    slug = models.SlugField('Slug', max_length=250, unique=True, blank=True)
    capa = models.ImageField('Capa', upload_to='capas/%Y/%m/', blank=True, null=True)
    capa_url = models.URLField('URL da Capa', max_length=500, blank=True)
    resumo = models.TextField('Resumo/Sinopse', blank=True)
    editora = models.CharField('Editora', max_length=100, blank=True)
    ano_publicacao = models.IntegerField(
        'Ano de Publicação', null=True, blank=True,
        validators=[MinValueValidator(1000), MaxValueValidator(timezone.now().year)],
    )
    paginas = models.IntegerField(
        'Número de Páginas', null=True, blank=True,
        validators=[MinValueValidator(1)],
    )

    # ===========================================
    # CLASSIFICAÇÃO
    # ===========================================
    genero = models.CharField(
        'Gênero', max_length=20,
        choices=GeneroLiterario.choices,
        db_index=True,
        default=GeneroLiterario.OUTROS,
    )
    idioma = models.CharField('Idioma', max_length=10, default='pt-BR')

    # ===========================================
    # STATUS E DISPONIBILIDADE
    # ===========================================
    status = models.CharField(
        'Status', max_length=2,
        choices=StatusLivro.choices,
        default=StatusLivro.DISPONIVEL_DOACAO,
        db_index=True,
    )
    tipo_midia = models.CharField(
        'Tipo de Mídia', max_length=2,
        choices=TipoMidia.choices,
        default=TipoMidia.FISICO,
    )

    # ===========================================
    # RECURSOS DE ACESSIBILIDADE
    # ===========================================
    possui_braille = models.BooleanField('Disponível em Braille', default=False)
    possui_fonte_ampliada = models.BooleanField('Disponível em Fonte Ampliada', default=False)
    possui_audio = models.BooleanField('Disponível em Áudio', default=False)
    possui_formato_digital_acessivel = models.BooleanField(
        'Formato Digital Acessível', default=False,
        help_text='PDF/EPUB acessível para leitores de tela',
    )

    # ===========================================
    # ARQUIVOS (para mídias digitais)
    # ===========================================
    arquivo_digital = models.FileField(
        'Arquivo Digital', upload_to='livros_digitais/%Y/%m/',
        blank=True, null=True,
    )
    arquivo_audio = models.FileField(
        'Arquivo de Áudio', upload_to='audiolivros/%Y/%m/',
        blank=True, null=True,
    )
    qr_code = models.ImageField(
        'QR Code', upload_to='qrcodes/%Y/%m/',
        blank=True, null=True,
    )

    # ===========================================
    # RELACIONAMENTOS
    # ===========================================
    doador = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True,
        related_name='livros_doados', verbose_name='Doador',
    )

    # ===========================================
    # AUDITORIA
    # ===========================================
    data_cadastro = models.DateTimeField('Data de Cadastro', auto_now_add=True, db_index=True)

    class Meta:
        verbose_name = 'Livro'
        verbose_name_plural = 'Livros'
        ordering = ['-data_cadastro']
        indexes = [
            models.Index(fields=['titulo']),
            models.Index(fields=['autor']),
            models.Index(fields=['isbn']),
            models.Index(fields=['genero']),
            models.Index(fields=['status']),
        ]

    def save(self, *args, **kwargs):
        """Gera slug e sanitiza dados antes de salvar."""
        # Gera slug único se ainda não existir
        if not self.slug:
            base_slug = generate_slug(self.titulo)
            slug = base_slug
            contador = 1
            # Garante unicidade
            while Livro.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f'{base_slug}-{contador}'
                contador += 1
            self.slug = slug

        # Sanitiza campos de texto (só se não forem None)
        if self.titulo:
            self.titulo = SecurityValidator.sanitize_html(self.titulo)
        if self.autor:
            self.autor = SecurityValidator.sanitize_html(self.autor)
        if self.resumo:
            self.resumo = SecurityValidator.sanitize_html(self.resumo)

        # Limpa ISBN (só números e X)
        if self.isbn:
            self.isbn = re.sub(r'[^0-9Xx]', '', self.isbn).upper()

        super().save(*args, **kwargs)

    @property
    def is_disponivel(self):
        """Verifica se o livro está disponível."""
        return self.status in ['DD', 'DE']

    @property
    def recursos_acessibilidade(self):
        """Lista de recursos de acessibilidade disponíveis."""
        recursos = []
        if self.possui_braille:
            recursos.append('Braille')
        if self.possui_fonte_ampliada:
            recursos.append('Fonte Ampliada')
        if self.possui_audio:
            recursos.append('Áudio')
        if self.possui_formato_digital_acessivel:
            recursos.append('Digital Acessível')
        return recursos

    def __str__(self):
        return f'{self.titulo} - {self.autor}'


class Avaliacao(BaseModel):
    """Avaliação de um livro feita por um usuário."""

    livro = models.ForeignKey(
        Livro, on_delete=models.CASCADE,
        related_name='avaliacoes', verbose_name='Livro',
    )
    usuario = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='avaliacoes', verbose_name='Usuário',
    )
    nota = models.IntegerField(
        'Nota',
        validators=[MinValueValidator(1), MaxValueValidator(5)],
    )
    comentario = models.TextField('Comentário', blank=True)
    data_avaliacao = models.DateTimeField('Data da Avaliação', auto_now_add=True, db_index=True)

    class Meta:
        verbose_name = 'Avaliação'
        verbose_name_plural = 'Avaliações'
        ordering = ['-data_avaliacao']
        unique_together = [['livro', 'usuario']]

    def __str__(self):
        return f'{self.usuario.username} - {self.livro.titulo} ({self.nota}★)'