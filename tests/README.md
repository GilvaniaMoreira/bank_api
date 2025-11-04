# Testes Unitários

Este diretório contém os testes unitários para a aplicação Bank API.


## Executando os Testes

### Executar todos os testes:
```bash
pytest
```

### Executar com detalhes:
```bash
pytest -v
```

### Executar com cobertura:
```bash
pytest --cov=src --cov-report=html
```

### Executar um arquivo específico:
```bash
pytest tests/test_service_account.py
```

### Executar uma classe específica:
```bash
pytest tests/test_service_account.py::TestAccountService
```

### Executar um teste específico:
```bash
pytest tests/test_service_account.py::TestAccountService::test_create_account_success
```

## Cobertura de Testes

Os testes cobrem:

- ✅ **Exceções**: Todas as exceções customizadas
- ✅ **Services**: AccountService e TransactionService
- ✅ **Controllers**: Controllers de accounts, transactions e auth
- ✅ **Security**: JWT, autenticação e autorização

## Fixtures Disponíveis

- `mock_database`: Mock do database
- `sample_account_record`: Registro de conta de exemplo
- `sample_account_in`: AccountIn de exemplo
- `sample_transaction_record`: Registro de transação de exemplo
- `sample_transaction_in_deposit`: TransactionIn de depósito
- `sample_transaction_in_withdrawal`: TransactionIn de saque
- `mock_record`: Factory para criar mocks de Record
- `mock_current_user`: Mock do usuário autenticado


