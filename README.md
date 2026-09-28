# 📚 Biblioteca do Saber

> Plataforma inclusiva de troca, doação e empréstimo de livros, com gamificação, acessibilidade e chat em tempo real.

[![Django](https://img.shields.io/badge/Django-4.2.7-092E20?style=flat&logo=django)](https://www.djangoproject.com/)
[![Python](https://img.shields.io/badge/Python-3.11-3776AB?style=flat&logo=python)](https://www.python.org/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-336791?style=flat&logo=postgresql)](https://www.postgresql.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

---

## 📖 Sobre o Projeto

A **Biblioteca do Saber** é uma plataforma web desenvolvida para promover a **economia circular do conhecimento**, permitindo que usuários:

- 📚 **Doem** livros que não usam mais
- 🔄 **Troquem** livros com outros leitores
- 📖 **Emprestem** livros temporariamente
- ⏳ **Reservem** livros populares (fila de espera)
- 🎮 **Ganhem pontos** por participação (gamificação)
- ♿ **Acessem** conteúdo com recursos de acessibilidade

### 🎯 Objetivos

- Democratizar o acesso à leitura
- Incentivar a economia circular
- Gamificar a participação (ranking, níveis, conquistas)
- Promover acessibilidade (VLibras, alto contraste, fonte dislexia)
- Criar uma comunidade de leitores

---

## ✨ Funcionalidades

### 🔐 Autenticação e Usuários
- Cadastro e login de usuários
- Perfil estendido (bio, avatar, endereço, telefone)
- Tipos de usuário: Leitor, Doador, Bibliotecário, Admin
- Recuperação de senha por email
- Proteção contra brute force (`django-axes`)

### 📚 Acervo
- Cadastro de livros com metadados completos
- Busca por título, autor ou ISBN
- Busca automática via **Google Books API**
- Recursos de acessibilidade (Braille, áudio, fonte ampliada)
- QR Code para cada livro
- Avaliações com nota (1-5 estrelas)

### 📖 Empréstimos
- Solicitação de empréstimo
- Aprovação pelo doador/bibliotecário
- Controle de status (Pendente, Aprovado, Recusado, Devolvido, Cancelado)
- Bloqueio de auto-empréstimo

### ⏳ Reservas
- Fila de espera para livros populares
- Cálculo automático de posição
- Notificação quando disponível
- Expiração automática (3 dias)

### 🎮 Gamificação
- Sistema de pontos por ação
- 8 ações: Doação, Empréstimo, Devolução, Avaliação, Cadastro, Convite, Leitura, Resenha
- 5 níveis: Novo Explorador → Mestre Bibliotecário
- Ranking geral
- Histórico de pontos

### 💬 Chat em Tempo Real
- Conversas entre usuários (WebSocket)
- Mensagens instantâneas
- Vinculação com livros específicos

### 📊 Dashboard
- Estatísticas pessoais
- Últimas atividades
- Posição no ranking
- Próxima conquista

### 🔔 Notificações
- Notificações por email
- Alertas de reserva confirmada/expirada
- Envio assíncrono (Celery)

### ♿ Acessibilidade
- VLibras (tradutor de Libras)
- Alto contraste
- Fonte para dislexia
- Controle de tamanho de fonte
- Navegação por teclado
- ARIA labels

### 📱 PWA
- Instalável como app
- Funciona offline (Service Worker)
- Manifest customizado

### 🌐 API REST
- Endpoints para todas as funcionalidades
- Autenticação JWT
- Filtros, busca e ordenação
- Paginação
- Documentação navegável

---

## 🛠️ Stack Tecnológico

### Backend
| Tecnologia | Versão | Uso |
|---|---|---|
| **Python** | 3.11+ | Linguagem principal |
| **Django** | 4.2.7 | Framework web |
| **Django REST Framework** | 3.14.0 | API REST |
| **PostgreSQL** | 15+ | Banco de dados |
| **Redis** | 7+ | Cache e broker |
| **Celery** | 5.3.4 | Tarefas assíncronas |
| **Channels** | 4.0.0 | WebSocket |

### Frontend
| Tecnologia | Uso |
|---|---|
| **HTML5 + CSS3** | Estrutura e estilo |
| **JavaScript (vanilla)** | Interações |
| **Bootstrap 5** | Design responsivo |
| **Crispy Forms** | Formulários |

### Infraestrutura
| Tecnologia | Uso |
|---|---|
| **Docker** | Containerização |
| **Docker Compose** | Orquestração |
| **Nginx** | Proxy reverso |
| **Gunicorn** | Servidor WSGI |
| **Daphne** | Servidor ASGI |
| **GitHub Actions** | CI/CD |

### Bibliotecas Principais
- `psycopg2-binary` — Driver PostgreSQL
- `dj-database-url` — Configuração de banco via URL
- `django-redis` — Cache Redis
- `channels-redis` — WebSocket com Redis
- `django-cors-headers` — CORS
- `django-axes` — Proteção brute force
- `django-ratelimit` — Rate limiting
- `bleach` — Sanitização HTML (XSS)
- `Pillow` — Processamento de imagens
- `qrcode` — Geração de QR Codes
- `pyzbar` — Leitura de QR Codes
- `scikit-learn` — Recomendações ML
- `pandas` / `numpy` — Análise de dados

---

## 📁 Estrutura do Projeto

```
biblioteca_do_saber/
├── 📄 manage.py
├── 📄 requirements.txt
├── 📄 Dockerfile
├── 📄 docker-compose.yml
├── 📄 Makefile
├── 📄 Procfile
├── 📄 .env.example
├── 📄 .gitignore
├── 📄 README.md
│
├── 📁 biblioteca_do_saber/       # Configurações
│   ├── asgi.py
│   ├── celery.py
│   ├── urls.py
│   ├── wsgi.py
│   └── settings/
│       ├── base.py
│       ├── development.py
│       └── production.py
│
├── 📁 apps/                       # 12 apps Django
│   ├── core/                      # Base, validators, mixins
│   ├── usuarios/                  # Perfis, autenticação
│   ├── acervo/                    # Livros, avaliações
│   ├── emprestimos/               # Empréstimos
│   ├── reservas/                  # Fila de espera
│   ├── gamificacao/               # Pontos, ranking
│   ├── notificacoes/              # Email, alertas
│   ├── chat/                      # WebSocket
│   ├── qrcode/                    # QR Codes
│   ├── recomendacao/              # Recomendações ML
│   ├── dashboard/                 # Painel do usuário
│   └── api/                       # REST API
│
├── 📁 templates/                  # Templates HTML
│   ├── base.html
│   ├── components/
│   └── (um diretório por app)
│
├── 📁 static/                     # Arquivos estáticos
│   ├── css/
│   ├── js/
│   ├── icons/
│   ├── manifest.json
│   └── sw.js
│
├── 📁 media/                      # Uploads de usuários
├── 📁 scripts/                    # Scripts auxiliares
├── 📁 deploy/                     # Configs de deploy
├── 📁 docs/                       # Documentação
└── 📁 .github/workflows/          # CI/CD
```

---

## 🚀 Como Rodar o Projeto

### Pré-requisitos

- **Python 3.11+**
- **PostgreSQL 15+**
- **Redis 7+** (opcional, para WebSocket/Celery)
- **Git**

### 1. Clonar o repositório

```
git clone https://github.com/seu-usuario/biblioteca-do-saber.git
cd biblioteca-do-saber
```

### 2. Criar ambiente virtual

```
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### 3. Instalar dependências

```
pip install -r requirements.txt
```

### 4. Configurar variáveis de ambiente

```
# Copiar o template
copy .env.example .env    # Windows
cp .env.example .env      # Linux/Mac
```

Editar o `.env` com suas credenciais:

```
SECRET_KEY=sua-chave-secreta-aqui
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

DATABASE_URL=postgresql://postgres:suasenha@localhost:5432/biblioteca_do_saber
POSTGRES_DB=biblioteca_do_saber
POSTGRES_USER=postgres
POSTGRES_PASSWORD=suasenha
POSTGRES_HOST=localhost
POSTGRES_PORT=5432

REDIS_URL=redis://localhost:6379/0
REDIS_CACHE_URL=redis://localhost:6379/1
REDIS_CHANNEL_URL=redis://localhost:6379/2

GOOGLE_BOOKS_API_KEY=sua-chave-google-books
```

### 5. Criar banco de dados

```
-- No PostgreSQL (via pgAdmin ou psql)
CREATE DATABASE biblioteca_do_saber;
```

### 6. Rodar migrações

```
python manage.py migrate
```

### 7. Popular dados iniciais

```
python scripts/run_populate.py
```

> ⚠️ **Importante:** rode este comando **antes** de criar usuários — ele cria as 8 ações de gamificação (Doação, Cadastro, Empréstimo, etc.).

### 8. Criar superusuário

```
python manage.py createsuperuser
```

### 9. Rodar o servidor

```
python manage.py runserver
```

Acesse: **http://127.0.0.1:8000/**

---

## 🐳 Rodando com Docker (Recomendado)

### 1. Subir os containers

```
docker-compose up -d
```

Isso sobe:
- **PostgreSQL** (porta 5432)
- **Redis** (porta 6379)
- **Django** (porta 8000)
- **Celery Worker**
- **Celery Beat**
- **Nginx** (porta 80)

### 2. Rodar migrações

```
docker-compose exec web python manage.py migrate
```

### 3. Popular dados

```
docker-compose exec web python scripts/run_populate.py
```

### 4. Criar superusuário

```
docker-compose exec web python manage.py createsuperuser
```

Acesse: **http://localhost/**

### 5. Comandos úteis

```
# Ver logs
docker-compose logs -f

# Parar containers
docker-compose down

# Reconstruir imagens
docker-compose build --no-cache
```

---

## 🧪 Testes

### Rodar todos os testes

```
pytest
```

### Com cobertura

```
pytest --cov=apps --cov-report=html
```

### Abrir relatório de cobertura

```
# Windows
start htmlcov/index.html

# Linux/Mac
open htmlcov/index.html
```

### Rodar testes de um app específico

```
pytest apps/acervo/
```

---

## 🌐 Endpoints da API

| Método | Endpoint | Descrição |
|---|---|---|
| GET | `/api/livros/` | Lista livros |
| GET | `/api/livros/{slug}/` | Detalhes do livro |
| POST | `/api/livros/` | Criar livro (autenticado) |
| GET | `/api/livros/acessiveis/` | Livros com Braille |
| GET | `/api/ranking/` | Ranking de usuários |
| GET | `/api/ranking/top10/` | Top 10 usuários |
| GET | `/api/emprestimos/` | Empréstimos do usuário |

### Filtros disponíveis

```
/api/livros/?genero=ROM&status=DD
/api/livros/?search=Dom Casmurro
/api/livros/?ordering=-data_cadastro
```

---

## 🔐 Segurança

O projeto inclui várias camadas de segurança:

- ✅ **HTTPS** em produção (HSTS, SSL redirect)
- ✅ **CSRF** protection
- ✅ **XSS** protection (bleach)
- ✅ **SQL Injection** protection (ORM Django)
- ✅ **Brute force** protection (django-axes)
- ✅ **Rate limiting** (django-ratelimit)
- ✅ **CORS** configurado
- ✅ **Security headers** customizados
- ✅ **Content Security Policy** (CSP)
- ✅ **Senhas fortes** (validators customizados)

---

## ♿ Acessibilidade

- 🦻 **VLibras** integrado (tradução de Libras)
- 🎨 **Alto contraste** (opcional)
- 📖 **Fonte para dislexia** (opcional)
- 🔍 **Controle de tamanho de fonte** (4 níveis)
- ⌨️ **Navegação por teclado**
- 🏷️ **ARIA labels** em elementos interativos
- 📝 **Textos alternativos** em imagens
- 🎯 **Foco visível** (WCAG 2.1)

## 🤝 Como Contribuir

1. **Fork** o projeto
2. Crie uma **branch** (`git checkout -b feature/nova-funcionalidade`)
3. **Commit** suas mudanças (`git commit -m 'Adiciona nova funcionalidade'`)
4. **Push** para a branch (`git push origin feature/nova-funcionalidade`)
5. Abra um **Pull Request**

### Padrões de código

- **Python:** PEP 8
- **Commits:** Conventional Commits
- **Testes:** obrigatórios para novas features
- **Documentação:** docstrings em funções públicas

---

## 🗺️ Roadmap

### ✅ Concluído (v1.0)
- [x] Sistema de usuários
- [x] Acervo de livros
- [x] Empréstimos
- [x] Reservas
- [x] Gamificação
- [x] Chat WebSocket
- [x] QR Code
- [x] Recomendações
- [x] Dashboard
- [x] API REST
- [x] Acessibilidade
- [x] PWA

---

## 📄 Licença

Este projeto está sob a licença **MIT**. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

---

## 👥 Autores

**Desenvolvedor Full Stack Júnior**

Carlos Eduardo Moreira Bardelotti RA 23203089

**Documentação Técnica**

Alex Junior Santos Martins RA 23202593

Ludimila da Silva Nishimura RA 2207841

Rafael Galisteu de Mello RA 2013616

Washington Aparecido Francisco de Paula RA 24214363

Wellington Gonçalves Noberto RA 1706278



---

## 🙏 Agradecimentos

- [Django](https://www.djangoproject.com/) — Framework web
- [Django REST Framework](https://www.django-rest-framework.org/) — API REST
- [PostgreSQL](https://www.postgresql.org/) — Banco de dados
- [Bootstrap](https://getbootstrap.com/) — Design
- [VLibras](https://vlibras.gov.br/) — Acessibilidade

---

## 📞 Contato

- **Email:** carlosbardelotti@gmail.com
- **Linkedin:** https://www.linkedin.com/in/carlos-eduardo-moreira-bardelotti-489b39a4/
- **GitHub:** https://github.com/BardelottiArquivos/biblioteca

---

<div align="center">

**⭐ Se este projeto foi útil, deixe uma estrela! ⭐**

**📚 Feito com ❤️ para democratizar a leitura 📚**

</div>

