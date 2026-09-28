# apps/qrcode/urls.py
from django.urls import path
from . import views

app_name = 'qrcode'

urlpatterns = [
    path('gerar/<int:livro_id>/', views.GerarQRCodeView.as_view(), name='gerar'),
]