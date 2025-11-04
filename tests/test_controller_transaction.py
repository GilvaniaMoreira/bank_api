"""Testes unitários para o controller de transações."""
import pytest
from unittest.mock import AsyncMock, MagicMock, patch

from src.schemas.transaction import TransactionIn
from src.models.transaction import TransactionType


@pytest.fixture
def mock_transaction_service():
    """Mock do TransactionService."""
    with patch("src.controller.transction.service") as mock:
        # Garante que o método é AsyncMock
        mock.create = AsyncMock()
        yield mock


@pytest.fixture
def mock_login_required():
    """Mock do login_required."""
    with patch("src.controller.transction.login_required", return_value=lambda: None) as mock:
        yield mock


class TestTransactionController:
    """Testes para o controller de transações."""

    @pytest.mark.asyncio
    async def test_create_transaction_success(self, mock_transaction_service):
        """Testa criação de transação com sucesso."""
        transaction_in = TransactionIn(
            account_id=1,
            type=TransactionType.DEPOSIT,
            amount=100.0
        )
        mock_record = MagicMock(
            id=1,
            account_id=1,
            type="deposit",
            amount=100.0,
            timestamp=None
        )
        mock_transaction_service.create = AsyncMock(return_value=mock_record)

        from src.controller.transction import create_transaction
        result = await create_transaction(transaction_in)

        assert result.id == 1
        assert result.account_id == 1
        assert result.type == "deposit"
        mock_transaction_service.create.assert_called_once_with(transaction_in)

    @pytest.mark.asyncio
    async def test_create_withdrawal_transaction(self, mock_transaction_service):
        """Testa criação de transação de saque."""
        transaction_in = TransactionIn(
            account_id=1,
            type=TransactionType.WITHDRAWAL,
            amount=50.0
        )
        mock_record = MagicMock(
            id=2,
            account_id=1,
            type="withdrawal",
            amount=50.0,
            timestamp=None
        )
        mock_transaction_service.create = AsyncMock(return_value=mock_record)

        from src.controller.transction import create_transaction
        result = await create_transaction(transaction_in)

        assert result.id == 2
        assert result.type == "withdrawal"
        assert result.amount == 50.0

