# apps/qrcode/views.py
from django.views.generic import View
from django.shortcuts import get_object_or_404, render

from apps.acervo.models import Livro
from .services import QRCodeGenerator


class GerarQRCodeView(View):
    def get(self, request, livro_id):
        livro = get_object_or_404(Livro, id=livro_id)
        resultado = QRCodeGenerator.gerar_qr_code(livro)
        return render(request, 'qrcode/gerar.html', {'livro': livro, 'qr': resultado})