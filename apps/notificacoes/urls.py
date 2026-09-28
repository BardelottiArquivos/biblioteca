# apps/notificacoes/urls.py
from django.urls import path
from . import views

app_name = 'notificacoes'

urlpatterns = [
    path('', views.ListaNotificacoesView.as_view(), name='lista'),
]