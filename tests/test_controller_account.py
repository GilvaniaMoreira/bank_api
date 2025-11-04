"""Testes unitários para o controller de contas."""
import pytest
from unittest.mock import AsyncMock, MagicMock, patch

from src.schemas.account import AccountIn


@pytest.fixture
def mock_account_service():
    """Mock do AccountService."""
    with patch("src.controller.account.account_service") as mock:
        # Garante que os métodos são AsyncMock
        mock.read_all = AsyncMock()
        mock.create = AsyncMock()
        yield mock


@pytest.fixture
def mock_transaction_service():
    """Mock do TransactionService."""
    with patch("src.controller.account.tx_service") as mock:
        # Garante que o método é AsyncMock
        mock.read_all = AsyncMock()
        yield mock


@pytest.fixture
def mock_login_required():
    """Mock do login_required."""
    with patch("src.controller.account.login_required", return_value=lambda: None) as mock:
        yield mock


class TestAccountController:
    """Testes para o controller de contas."""

    @pytest.mark.asyncio
    async def test_read_accounts_success(self, mock_account_service):
        """Testa leitura de contas com sucesso."""
        mock_records = [
            MagicMock(id=1, user_id=123, balance=1000.0, created_at=None),
            MagicMock(id=2, user_id=456, balance=500.0, created_at=None),
        ]
        mock_account_service.read_all = AsyncMock(return_value=mock_records)

        from src.controller.account import read_accounts
        result = await read_accounts(limit=10, skip=0)

        assert len(result) == 2
        assert result[0].id == 1
        assert result[1].id == 2
        mock_account_service.read_all.assert_called_once_with(limit=10, skip=0)

    @pytest.mark.asyncio
    async def test_read_accounts_with_pagination(self, mock_account_service):
        """Testa leitura de contas com paginação."""
        mock_records = []
        mock_account_service.read_all = AsyncMock(return_value=mock_records)

        from src.controller.account import read_accounts
        result = await read_accounts(limit=5, skip=10)

        assert result == []
        mock_account_service.read_all.assert_called_once_with(limit=5, skip=10)

    @pytest.mark.asyncio
    async def test_create_account_success(self, mock_account_service):
        """Testa criação de conta com sucesso."""
        account_in = AccountIn(user_id=123, balance=1000.0)
        mock_record = MagicMock(id=1, user_id=123, balance=1000.0, created_at=None)
        mock_account_service.create = AsyncMock(return_value=mock_record)

        from src.controller.account import create_account
        result = await create_account(account_in)

        assert result.id == 1
        assert result.user_id == 123
        mock_account_service.create.assert_called_once_with(account_in)

    @pytest.mark.asyncio
    async def test_read_account_transactions_success(self, mock_transaction_service):
        """Testa leitura de transações de uma conta com sucesso."""
        mock_records = [
            MagicMock(id=1, account_id=1, type="deposit", amount=100.0, timestamp=None),
            MagicMock(id=2, account_id=1, type="withdrawal", amount=50.0, timestamp=None),
        ]
        mock_transaction_service.read_all = AsyncMock(return_value=mock_records)

        from src.controller.account import read_account_transactions
        result = await read_account_transactions(id=1, limit=10, skip=0)

        assert len(result) == 2
        assert result[0].account_id == 1
        mock_transaction_service.read_all.assert_called_once_with(account_id=1, limit=10, skip=0)

    @pytest.mark.asyncio
    async def test_read_account_transactions_empty(self, mock_transaction_service):
        """Testa leitura de transações quando não há transações."""
        mock_transaction_service.read_all = AsyncMock(return_value=[])

        from src.controller.account import read_account_transactions
        result = await read_account_transactions(id=1, limit=10, skip=0)

        assert result == []

