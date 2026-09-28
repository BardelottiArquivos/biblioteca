# apps/recomendacao/urls.py
from django.urls import path
from . import views

app_name = 'recomendacao'

urlpatterns = [
    path('', views.RecomendacoesView.as_view(), name='lista'),
]