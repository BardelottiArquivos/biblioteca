# apps/chat/urls.py
from django.urls import path
from . import views

app_name = 'chat'

urlpatterns = [
    path('', views.ListaConversasView.as_view(), name='lista'),
    path('<int:conversa_id>/', views.ConversaView.as_view(), name='conversa'),
]