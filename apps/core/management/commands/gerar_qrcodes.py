from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Gera QR Codes em massa para livros sem QR Code'

    def add_arguments(self, parser):
        parser.add_argument('--todos', action='store_true',
                            help='Gera QR Code para todos os livros, mesmo os que já têm')

    def handle(self, *args, **options):
        # Imports dentro do handle para evitar erros se o app não estiver migrado
        from apps.acervo.models import Livro
        from apps.qrcode.services import QRCodeGenerator

        if options['todos']:
            livros = Livro.objects.all()
        else:
            # Filtra livros sem QR code (nulo ou vazio)
            livros = Livro.objects.filter(qr_code='') | Livro.objects.filter(qr_code__isnull=True)

        total = livros.count()
        self.stdout.write(f'Gerando QR Codes para {total} livro(s)...')

        sucessos = 0
        for livro in livros:
            resultado = QRCodeGenerator.gerar_qr_code(livro)
            if resultado:
                sucessos += 1
                self.stdout.write(self.style.SUCCESS(f'  ✓ {livro.titulo}'))

        self.stdout.write(self.style.SUCCESS(f'\n{sucessos}/{total} QR Codes gerados!'))
