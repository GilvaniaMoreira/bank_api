"""Fixtures compartilhadas para testes."""
import os
import sys
import asyncio
from datetime import datetime
from decimal import Decimal
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
import sqlalchemy as sa

# Define variáveis de ambiente de teste antes de importar qualquer módulo
os.environ.setdefault("DATABASE_URL", "postgresql://test:test@localhost/test")
os.environ.setdefault("ENVIRONMENT", "test")

# Mocka o Database antes de importar src.database para evitar tentativa de conexão
mock_db_instance = MagicMock()
mock_db_instance.transaction = MagicMock(return_value=lambda func: func)
mock_db_instance.fetch_all = AsyncMock()
mock_db_instance.fetch_one = AsyncMock()
mock_db_instance.execute = AsyncMock()
mock_db_instance.connect = AsyncMock()
mock_db_instance.disconnect = AsyncMock()

# Cria um metadata REAL do SQLAlchemy para os modelos funcionarem
test_metadata = sa.MetaData()

# Cria um mock do módulo database antes de ser importado
class MockDatabaseModule:
    """Mock do módulo database."""
    def __init__(self):
        self.database = mock_db_instance
        self.metadata = test_metadata

# Insere o mock no sys.modules antes de qualquer importação que use database
sys.modules['src.database'] = MockDatabaseModule()

# Agora podemos importar os módulos que dependem do database
from src.schemas.account import AccountIn
from src.schemas.transaction import TransactionIn
from src.models.transaction import TransactionType


# Removido event_loop fixture - pytest-asyncio fornece automaticamente


@pytest.fixture
def mock_database():
    """Mock do database."""
    # Retorna o mock já criado no nível do módulo
    return mock_db_instance


@pytest.fixture
def sample_account_record() -> dict:
    """Retorna um registro de conta de exemplo."""
    return {
        "id": 1,
        "user_id": 123,
        "balance": Decimal("1000.00"),
        "created_at": datetime(2024, 1, 1, 12, 0, 0),
    }


@pytest.fixture
def sample_account_in() -> AccountIn:
    """Retorna um AccountIn de exemplo."""
    return AccountIn(user_id=123, balance=1000.0)


@pytest.fixture
def sample_transaction_record() -> dict:
    """Retorna um registro de transação de exemplo."""
    return {
        "id": 1,
        "account_id": 1,
        "type": "deposit",
        "amount": Decimal("100.00"),
        "timestamp": datetime(2024, 1, 1, 12, 0, 0),
    }


@pytest.fixture
def sample_transaction_in_deposit() -> TransactionIn:
    """Retorna um TransactionIn de depósito."""
    return TransactionIn(
        account_id=1,
        type=TransactionType.DEPOSIT,
        amount=100.0
    )


@pytest.fixture
def sample_transaction_in_withdrawal() -> TransactionIn:
    """Retorna um TransactionIn de saque."""
    return TransactionIn(
        account_id=1,
        type=TransactionType.WITHDRAWAL,
        amount=50.0
    )


@pytest.fixture
def mock_record():
    """Cria um mock de Record."""
    def _create_mock_record(data: dict):
        record = MagicMock()
        for key, value in data.items():
            setattr(record, key, value)
        return record
    return _create_mock_record


@pytest.fixture
def mock_current_user():
    """Mock do usuário atual autenticado."""
    return {"user_id": 123}

