# apps/reservas/urls.py
from django.urls import path
from . import views

app_name = 'reservas'

urlpatterns = [
    path('', views.ListaReservasView.as_view(), name='lista'),
    path('criar/<slug:slug>/', views.CriarReservaView.as_view(), name='criar'),
    path('<int:pk>/cancelar/', views.CancelarReservaView.as_view(), name='cancelar'),
]