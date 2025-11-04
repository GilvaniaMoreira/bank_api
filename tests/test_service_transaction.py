"""Testes unitários para TransactionService."""
import pytest
from decimal import Decimal
from unittest.mock import AsyncMock, MagicMock, patch

from src.exceptions import AccountNotFoundError, InsufficientBalanceError
from src.service.transaction import TransactionService
from src.schemas.transaction import TransactionIn
from src.models.transaction import TransactionType


class TestTransactionService:
    """Testes para TransactionService."""

    @pytest.fixture
    def transaction_service(self):
        """Cria uma instância do TransactionService."""
        return TransactionService()

    @pytest.mark.asyncio
    async def test_read_all_success(
        self, transaction_service, mock_database, sample_transaction_record
    ):
        """Testa leitura de transações com sucesso."""
        mock_records = [MagicMock(**sample_transaction_record)]
        mock_database.fetch_all = AsyncMock(return_value=mock_records)

        result = await transaction_service.read_all(account_id=1, limit=10, skip=0)

        assert len(result) == 1
        assert result[0].account_id == 1
        mock_database.fetch_all.assert_called_once()

    @pytest.mark.asyncio
    async def test_create_deposit_success(
        self, transaction_service, mock_database, sample_transaction_in_deposit
    ):
        """Testa criação de depósito com sucesso."""
        account_record = {
            "id": 1,
            "user_id": 123,
            "balance": Decimal("1000.00"),
            "created_at": None,
        }
        mock_account = MagicMock(**account_record)
        mock_database.fetch_one = AsyncMock(return_value=mock_account)
        mock_database.execute = AsyncMock(return_value=1)

        transaction_record = {
            "id": 1,
            "account_id": 1,
            "type": "deposit",
            "amount": Decimal("100.00"),
            "timestamp": None,
        }
        mock_transaction = MagicMock(**transaction_record)
        mock_database.fetch_one.side_effect = [mock_account, mock_transaction]

        result = await transaction_service.create(sample_transaction_in_deposit)

        assert result.id == 1
        assert result.type == "deposit"
        assert mock_database.execute.call_count == 2  # insert transaction + update account

    @pytest.mark.asyncio
    async def test_create_withdrawal_success(
        self, transaction_service, mock_database, sample_transaction_in_withdrawal
    ):
        """Testa criação de saque com sucesso."""
        account_record = {
            "id": 1,
            "user_id": 123,
            "balance": Decimal("1000.00"),
            "created_at": None,
        }
        mock_account = MagicMock(**account_record)
        mock_database.fetch_one = AsyncMock(return_value=mock_account)
        mock_database.execute = AsyncMock(return_value=1)

        transaction_record = {
            "id": 1,
            "account_id": 1,
            "type": "withdrawal",
            "amount": Decimal("50.00"),
            "timestamp": None,
        }
        mock_transaction = MagicMock(**transaction_record)
        mock_database.fetch_one.side_effect = [mock_account, mock_transaction]

        result = await transaction_service.create(sample_transaction_in_withdrawal)

        assert result.id == 1
        assert result.type == "withdrawal"
        assert mock_database.execute.call_count == 2

    @pytest.mark.asyncio
    async def test_create_withdrawal_insufficient_balance(
        self, transaction_service, mock_database
    ):
        """Testa saque com saldo insuficiente."""
        transaction_in = TransactionIn(
            account_id=1,
            type=TransactionType.WITHDRAWAL,
            amount=1500.0
        )

        account_record = {
            "id": 1,
            "user_id": 123,
            "balance": Decimal("1000.00"),
            "created_at": None,
        }
        mock_account = MagicMock(**account_record)
        mock_database.fetch_one = AsyncMock(return_value=mock_account)

        with pytest.raises(InsufficientBalanceError) as exc_info:
            await transaction_service.create(transaction_in)

        assert exc_info.value.account_id == 1
        assert exc_info.value.balance == 1000.0
        assert "Insufficient balance" in str(exc_info.value)

    @pytest.mark.asyncio
    async def test_create_transaction_account_not_found(
        self, transaction_service, mock_database, sample_transaction_in_deposit
    ):
        """Testa criação de transação com conta não encontrada."""
        mock_database.fetch_one = AsyncMock(return_value=None)

        with pytest.raises(AccountNotFoundError) as exc_info:
            await transaction_service.create(sample_transaction_in_deposit)

        assert exc_info.value.account_id == 1
        assert "Account with ID 1 not found" in str(exc_info.value)

    @pytest.mark.asyncio
    async def test_create_withdrawal_exact_balance(
        self, transaction_service, mock_database
    ):
        """Testa saque com valor exato do saldo."""
        transaction_in = TransactionIn(
            account_id=1,
            type=TransactionType.WITHDRAWAL,
            amount=1000.0
        )

        account_record = {
            "id": 1,
            "user_id": 123,
            "balance": Decimal("1000.00"),
            "created_at": None,
        }
        mock_account = MagicMock(**account_record)
        mock_database.fetch_one = AsyncMock(return_value=mock_account)
        mock_database.execute = AsyncMock(return_value=1)

        transaction_record = {
            "id": 1,
            "account_id": 1,
            "type": "withdrawal",
            "amount": Decimal("1000.00"),
            "timestamp": None,
        }
        mock_transaction = MagicMock(**transaction_record)
        mock_database.fetch_one.side_effect = [mock_account, mock_transaction]

        result = await transaction_service.create(transaction_in)

        assert result.id == 1
        assert mock_database.execute.call_count == 2

    @pytest.mark.asyncio
    async def test_read_all_empty_result(
        self, transaction_service, mock_database
    ):
        """Testa leitura de transações quando não há resultados."""
        mock_database.fetch_all = AsyncMock(return_value=[])

        result = await transaction_service.read_all(account_id=999, limit=10, skip=0)

        assert result == []
        mock_database.fetch_all.assert_called_once()


