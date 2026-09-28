# apps/emprestimos/urls.py
from django.urls import path
from . import views

app_name = 'emprestimos'

urlpatterns = [
    path('', views.ListaEmprestimosView.as_view(), name='lista'),
    path('<int:pk>/', views.DetalhesEmprestimoView.as_view(), name='detalhes'),
    path('solicitar/<slug:slug>/', views.SolicitarEmprestimoView.as_view(), name='solicitar'),
]