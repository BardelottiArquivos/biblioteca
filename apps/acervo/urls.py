# apps/acervo/urls.py
from django.urls import path
from . import views

app_name = 'acervo'

urlpatterns = [
    path('', views.AcervoListView.as_view(), name='lista'),
    path('cadastrar/', views.CadastrarLivroView.as_view(), name='cadastrar'),
    path('buscar-isbn/', views.BuscarISBNView.as_view(), name='buscar_isbn'),
    path('<slug:slug>/', views.LivroDetailView.as_view(), name='detalhes'),
]
