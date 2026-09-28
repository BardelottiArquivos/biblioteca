# apps/usuarios/urls.py
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'usuarios'

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(
        template_name='usuarios/login.html'
    ), name='login'),
    path('logout/', auth_views.LogoutView.as_view(
        next_page='core:home'
    ), name='logout'),
    path('cadastro/', views.CadastroView.as_view(), name='cadastro'),
    path('perfil/', views.PerfilView.as_view(), name='perfil'),
    path('perfil/editar/', views.EditarPerfilView.as_view(), name='editar_perfil'),

    # Recuperação de senha
    path('senha/recuperar/', auth_views.PasswordResetView.as_view(
        template_name='usuarios/recuperar_senha.html',
        email_template_name='emails/recuperar_senha.html',
        success_url='/usuarios/senha/recuperar/enviado/',
    ), name='password_reset'),
    path('senha/recuperar/enviado/', auth_views.PasswordResetDoneView.as_view(
        template_name='usuarios/senha_enviada.html',
    ), name='password_reset_done'),
]