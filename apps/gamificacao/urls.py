# apps/gamificacao/urls.py
from django.urls import path
from . import views

app_name = 'gamificacao'

urlpatterns = [
    path('ranking/', views.RankingView.as_view(), name='ranking'),
    path('meu-progresso/', views.MeuProgressoView.as_view(), name='meu_progresso'),
    path('como-funciona/', views.ComoFuncionaView.as_view(), name='como_funciona'),
]