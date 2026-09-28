# apps/api/serializers.py
from rest_framework import serializers

from apps.acervo.models import Livro
from apps.gamificacao.models import PontuacaoUsuario
from apps.emprestimos.models import SolicitacaoEmprestimo


class LivroSerializer(serializers.ModelSerializer):
    doador_nome = serializers.CharField(source='doador.username', read_only=True)
    recursos_acessibilidade = serializers.ReadOnlyField()

    class Meta:
        model = Livro
        fields = [
            'id', 'titulo', 'autor', 'isbn', 'resumo', 'editora',
            'ano_publicacao', 'paginas', 'genero', 'idioma',
            'status', 'tipo_midia', 'possui_braille',
            'possui_fonte_ampliada', 'possui_audio',
            'possui_formato_digital_acessivel',
            'capa_url', 'slug', 'doador_nome',
            'recursos_acessibilidade', 'data_cadastro',
        ]
        read_only_fields = ['id', 'slug', 'data_cadastro']


class PontuacaoUsuarioSerializer(serializers.ModelSerializer):
    usuario_nome = serializers.CharField(source='usuario.username', read_only=True)

    class Meta:
        model = PontuacaoUsuario
        fields = ['id', 'usuario', 'usuario_nome', 'pontos_totais', 'nivel', 'titulo']
        read_only_fields = ['id']


class EmprestimoSerializer(serializers.ModelSerializer):
    solicitante_nome = serializers.CharField(source='solicitante.username', read_only=True)
    livro_titulo = serializers.CharField(source='livro.titulo', read_only=True)

    class Meta:
        model = SolicitacaoEmprestimo
        fields = [
            'id', 'solicitante', 'solicitante_nome', 'livro', 'livro_titulo',
            'status', 'data_solicitacao', 'data_aprovacao', 'data_devolucao',
            'observacoes',
        ]
        read_only_fields = [
            'id', 'data_solicitacao', 'data_aprovacao', 'data_devolucao',
        ]