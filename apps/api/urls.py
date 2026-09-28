# apps/api/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import LivroViewSet, RankingViewSet, EmprestimoViewSet

router = DefaultRouter()
router.register('livros', LivroViewSet, basename='livro')
router.register('ranking', RankingViewSet, basename='ranking')
router.register('emprestimos', EmprestimoViewSet, basename='emprestimo')

app_name = 'api'

urlpatterns = [
    # CORRIGIDO: era 'routers.urls' (plural) — o correto é 'router.urls'
    path('', include(router.urls)),
]