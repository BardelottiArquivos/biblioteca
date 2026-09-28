# scripts/run_populate.py
# ==============================================
# POPULA DADOS INICIAIS NO BANCO
# ==============================================
import os
import sys
import django


def setup_django():
    """Configura o Django antes de importar modelos."""
    os.environ.setdefault(
        'DJANGO_SETTINGS_MODULE',
        'biblioteca_do_saber.settings.development'
    )
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    sys.path.append(base_dir)
    django.setup()
    print('✅ Django configurado!')


def popular_acoes():
    """Popula as ações de gamificação."""
    from apps.gamificacao.models import Acao

    acoes = [
        {'tipo': 'DOACAO',    'pontos': 50, 'descricao': 'Doar um livro',           'icone': '📚'},
        {'tipo': 'EMPRESTIMO','pontos': 30, 'descricao': 'Realizar empréstimo',      'icone': '📖'},
        {'tipo': 'DEVOLUCAO', 'pontos': 20, 'descricao': 'Devolver no prazo',        'icone': '✅'},
        {'tipo': 'AVALIACAO', 'pontos': 10, 'descricao': 'Avaliar um livro',         'icone': '⭐'},
        {'tipo': 'CADASTRO',  'pontos': 20, 'descricao': 'Cadastrar na plataforma',  'icone': '🎉'},
        {'tipo': 'CONVITE',   'pontos': 15, 'descricao': 'Convidar um amigo',        'icone': '👥'},
        {'tipo': 'LEITURA',   'pontos': 5,  'descricao': 'Registrar uma leitura',    'icone': '📕'},
        {'tipo': 'RESENHA',   'pontos': 25, 'descricao': 'Publicar uma resenha',     'icone': '✍️'},
    ]

    criados = 0
    for acao in acoes:
        obj, created = Acao.objects.get_or_create(
            tipo=acao['tipo'], defaults=acao,
        )
        if created:
            criados += 1
            print(f'  ✅ {acao["icone"]} {acao["tipo"]} - {acao["pontos"]} pts')
        else:
            print(f'  ℹ️  {acao["icone"]} {acao["tipo"]} - já existe')

    return criados


def main():
    print('=' * 60)
    print('POPULANDO DADOS INICIAIS - BIBLIOTECA DO SABER')
    print('=' * 60)

    try:
        print('\n📊 Populando ações de gamificação...')
        total_acoes = popular_acoes()
        print(f'\n✅ {total_acoes} ações criadas com sucesso!')

        print('\n🎉 População concluída!')
        return True

    except Exception as e:
        print(f'\n❌ ERRO: {str(e)}')
        import traceback
        traceback.print_exc()
        return False


if __name__ == '__main__':
    try:
        setup_django()
        sucesso = main()
        sys.exit(0 if sucesso else 1)
    except Exception as e:
        print(f'\n❌ Erro fatal: {str(e)}')
        sys.exit(1)
