# apps/qrcode/services.py
# ============================================
# SERVIÇOS DE QR CODE
# ============================================
import logging
import re
from io import BytesIO

import qrcode
from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles.moduledrawers import RoundedModuleDrawer
from qrcode.image.styles.colormasks import SolidFillColorMask
from qrcode import constants as qrcode_constants

from django.conf import settings  # CORRIGIDO: era 'setting' (singular)
from django.core.files.base import ContentFile

from apps.acervo.models import Livro

logger = logging.getLogger(__name__)


class QRCodeGenerator:
    """Gerador de QR Codes estilizados para livros."""

    @staticmethod
    def gerar_qr_code(livro):
        """Gera QR Code para um livro específico."""
        try:
            base_url = getattr(settings, 'BASE_URL', 'http://localhost:8000')
            url = f'{base_url}/acervo/{livro.slug}/'

            qr = qrcode.QRCode(
                version=3,
                error_correction=qrcode_constants.ERROR_CORRECT_H,
                box_size=10,
                border=4,
            )
            qr.add_data(url)
            qr.make(fit=True)

            img = qr.make_image(
                image_factory=StyledPilImage,
                module_drawer=RoundedModuleDrawer(),
                color_mask=SolidFillColorMask(
                    front_color=(44, 107, 143),
                    back_color=(255, 255, 255),
                ),
            )

            buffer = BytesIO()
            img.save(buffer, format='PNG')
            buffer.seek(0)

            filename = f'qr_code_{livro.id}.png'
            livro.qr_code.save(filename, ContentFile(buffer.getvalue()), save=True)

            logger.info(f'QR Code gerado para {livro.titulo}')
            return {'url': livro.qr_code.url if livro.qr_code else None}

        except Exception as e:
            logger.error(f'Erro ao gerar QR Code: {str(e)}')
            return None

    @staticmethod
    def gerar_qr_code_massa(livros):
        """Gera QR Codes em massa."""
        resultados = []
        for livro in livros:
            try:
                resultado = QRCodeGenerator.gerar_qr_code(livro)
                resultados.append({
                    'livro': livro.titulo,
                    'sucesso': True,
                    'qr_code': resultado,
                })
            except Exception as e:
                resultados.append({
                    'livro': livro.titulo,
                    'sucesso': False,
                    'erro': str(e),
                })
        return resultados


class LeitorQRCode:
    """Leitor de QR Code para catalogação rápida."""

    @staticmethod
    def processar_qr_code(imagem):
        try:
            from pyzbar.pyzbar import decode
            from PIL import Image

            img = Image.open(imagem)
            decoded_objects = decode(img)

            if decoded_objects:
                qr_data = decoded_objects[0].data.decode('utf-8')
                match = re.search(r'/acervo/([^/]+)/', qr_data)

                if match:
                    slug = match.group(1)
                    try:
                        livro = Livro.objects.get(slug=slug)
                        return {
                            'sucesso': True,
                            'livro': {
                                'id': livro.id,
                                'titulo': livro.titulo,
                                'autor': livro.autor,
                                'isbn': livro.isbn,
                            },
                        }
                    except Livro.DoesNotExist:
                        return {'sucesso': False, 'erro': 'Livro não encontrado'}

                return {'sucesso': False, 'erro': 'QR Code inválido'}

            return {'sucesso': False, 'erro': 'Nenhum QR Code encontrado'}

        except Exception as e:
            logger.error(f'Erro ao processar QR Code: {str(e)}')
            return {'sucesso': False, 'erro': str(e)}