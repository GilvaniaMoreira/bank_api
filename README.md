# Bank API

Microserviço para gerenciar operações de depósito e saque em contas correntes.

## Descrição

A Bank API é uma API REST desenvolvida com FastAPI que permite o gerenciamento de contas correntes e transações bancárias. O sistema oferece funcionalidades completas para criação de contas, registro de transações (depósitos e saques), autenticação via JWT e consulta de histórico de transações.

## Funcionalidades

- **Autenticação**: Sistema de autenticação baseado em JWT
- **Gerenciamento de Contas**: 
  - Criação de contas correntes
  - Listagem de contas
  - Consulta de saldo
- **Transações**:
  - Realização de depósitos
  - Realização de saques
  - Validação de saldo suficiente
  - Histórico de transações por conta

## Tecnologias Utilizadas

- **FastAPI**: Framework web moderno e rápido para construção de APIs
- **SQLAlchemy**: ORM para Python
- **Databases**: Biblioteca assíncrona para conexão com banco de dados
- **PostgreSQL**: Banco de dados relacional (configurável)
- **SQLite**: Banco de dados padrão para desenvolvimento
- **Pydantic**: Validação de dados e configurações
- **JWT (PyJWT)**: Autenticação baseada em tokens
- **Alembic**: Ferramenta de migração de banco de dados
- **Poetry**: Gerenciamento de dependências e ambiente

## Pré-requisitos

- Python 3.10 ou superior
- Poetry (para gerenciamento de dependências)
- PostgreSQL (opcional, para produção)

## Instalação

1. **Clone o repositório**:
```bash
git clone <url-do-repositório>
cd bank_api
```

2. **Instale as dependências usando Poetry**:
```bash
poetry install
```

3. **Ative o ambiente virtual**:
```bash
poetry shell
```

## Configuração

Crie um arquivo `.env` na raiz do projeto com as seguintes variáveis de ambiente:

```env
DATABASE_URL=postgresql://usuario:senha@localhost:5432/bank_db
# Ou para SQLite (padrão):
# DATABASE_URL=sqlite+aiosqlite:///./bank.db

ENVIRONMENT=development
```

**Variáveis disponíveis:**
- `DATABASE_URL`: URL de conexão com o banco de dados (padrão: `sqlite+aiosqlite:///:memory:`)
- `ENVIRONMENT`: Ambiente de execução (`development` ou `production`)

## Executando a Aplicação

Para iniciar o servidor de desenvolvimento:

```bash
uvicorn src.main:app --reload
```

A aplicação estará disponível em `http://localhost:8000`

### Documentação Interativa

- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc` (desabilitado por padrão)

## Endpoints da API

### Autenticação

#### `POST /auth/login`
Autentica um usuário e retorna um token JWT.

**Request Body:**
```json
{
  "user_id": 1
}
```

**Response:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

### Contas

#### `GET /accounts/`
Lista todas as contas (requer autenticação).

**Query Parameters:**
- `limit` (obrigatório): Número máximo de resultados
- `skip` (opcional): Número de resultados para pular (padrão: 0)

**Headers:**
```
Authorization: Bearer <token>
```

#### `POST /accounts/`
Cria uma nova conta (requer autenticação).

**Request Body:**
```json
{
  "user_id": 1,
  "balance": 0.00
}
```

**Response:** 201 Created
```json
{
  "id": 1,
  "user_id": 1,
  "balance": 0.00,
  "created_at": "2024-01-01T12:00:00Z"
}
```

#### `GET /accounts/{id}/transactions`
Lista todas as transações de uma conta específica (requer autenticação).

**Query Parameters:**
- `limit` (obrigatório): Número máximo de resultados
- `skip` (opcional): Número de resultados para pular (padrão: 0)

**Headers:**
```
Authorization: Bearer <token>
```

### Transações

#### `POST /transactions/`
Cria uma nova transação (depósito ou saque) (requer autenticação).

**Request Body:**
```json
{
  "account_id": 1,
  "type": "deposit",
  "amount": 100.00
}
```

**Tipos de transação:**
- `deposit`: Depósito (adiciona valor ao saldo)
- `withdrawal`: Saque (subtrai valor do saldo)

**Response:** 201 Created
```json
{
  "id": 1,
  "account_id": 1,
  "type": "deposit",
  "amount": 100.00,
  "timestamp": "2024-01-01T12:00:00Z"
}
```

## Autenticação

A API utiliza autenticação baseada em JWT (JSON Web Tokens). Para acessar os endpoints protegidos:

1. Faça login em `/auth/login` fornecendo um `user_id`
2. Copie o `access_token` retornado
3. Inclua o token no header das requisições:
```
Authorization: Bearer <seu_token>
```

## Tratamento de Erros

A API retorna códigos de status HTTP apropriados e mensagens de erro descritivas:

- **400 Bad Request**: Valores inválidos (ex: valor negativo, tipo de transação inválido)
- **404 Not Found**: Conta ou transação não encontrada
- **409 Conflict**: Erros de negócio (ex: saldo insuficiente para saque)

**Exemplo de resposta de erro:**
```json
{
  "detail": "Saldo insuficiente para realizar o saque"
}
```

## Testes

O projeto inclui uma suíte completa de testes unitários. Para executar:

```bash
# Executar todos os testes
pytest

# Executar com detalhes
pytest -v

# Executar com cobertura de código
pytest --cov=src --cov-report=html

# Executar um arquivo específico
pytest tests/test_service_account.py
```

### Cobertura de Testes

Os testes cobrem:
- Exceções customizadas
- Services (AccountService e TransactionService)
- Controllers (accounts, transactions e auth)
- Security (JWT, autenticação e autorização)

Para mais informações sobre os testes, consulte `tests/README.md`.

## Migrações do Banco de Dados

O projeto utiliza Alembic para gerenciar migrações do banco de dados:

```bash
# Criar uma nova migração
alembic revision --autogenerate -m "Descrição da migração"

# Aplicar migrações
alembic upgrade head

# Reverter última migração
alembic downgrade -1
```

## Arquitetura

O projeto segue uma arquitetura em camadas:

- **Controllers**: Camada de controle que recebe requisições HTTP e delega para os services
- **Services**: Lógica de negócio e validações
- **Models**: Definição das tabelas do banco de dados (SQLAlchemy)
- **Schemas**: Modelos Pydantic para validação de entrada e saída
- **Views**: Modelos Pydantic para respostas da API
- **Security**: Funções de autenticação e autorização JWT
- **Database**: Configuração e conexão com o banco de dados

## Desenvolvimento

### Formatação de Código

O projeto utiliza Black e Ruff para formatação e linting:

```bash
# Formatar código
black src tests

# Verificar linting
ruff check src tests

# Verificar tipos
mypy src
```


## Licença

Este projeto está sob licença MIT.


