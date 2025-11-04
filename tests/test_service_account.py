"""Testes unitários para AccountService."""
import pytest
from unittest.mock import AsyncMock, MagicMock, patch

from src.exceptions import AccountNotFoundError
from src.service.account import AccountService
from src.schemas.account import AccountIn


class TestAccountService:
    """Testes para AccountService."""

    @pytest.fixture
    def account_service(self):
        """Cria uma instância do AccountService."""
        return AccountService()

    @pytest.mark.asyncio
    async def test_read_all_success(
        self, account_service, mock_database, sample_account_record
    ):
        """Testa leitura de todas as contas com sucesso."""
        mock_records = [MagicMock(**sample_account_record)]
        mock_database.fetch_all = AsyncMock(return_value=mock_records)

        result = await account_service.read_all(limit=10, skip=0)

        assert len(result) == 1
        assert result[0].id == 1
        mock_database.fetch_all.assert_called_once()

    @pytest.mark.asyncio
    async def test_read_all_with_pagination(
        self, account_service, mock_database
    ):
        """Testa leitura de contas com paginação."""
        mock_records = []
        mock_database.fetch_all = AsyncMock(return_value=mock_records)

        result = await account_service.read_all(limit=5, skip=10)

        assert result == []
        mock_database.fetch_all.assert_called_once()

    @pytest.mark.asyncio
    async def test_create_account_success(
        self, account_service, mock_database, sample_account_in, sample_account_record
    ):
        """Testa criação de conta com sucesso."""
        account_id = 1
        mock_database.execute = AsyncMock(return_value=account_id)
        mock_record = MagicMock(**sample_account_record)
        mock_database.fetch_one = AsyncMock(return_value=mock_record)

        result = await account_service.create(sample_account_in)

        assert result.id == 1
        assert result.user_id == 123
        mock_database.execute.assert_called_once()
        mock_database.fetch_one.assert_called_once()

    @pytest.mark.asyncio
    async def test_create_account_with_zero_balance(
        self, account_service, mock_database
    ):
        """Testa criação de conta com saldo zero."""
        # PositiveFloat não aceita 0, então testamos com um valor mínimo válido
        account_in = AccountIn(user_id=456, balance=0.01)
        account_id = 2
        mock_database.execute = AsyncMock(return_value=account_id)
        
        account_record = {
            "id": account_id,
            "user_id": 456,
            "balance": 0.01,
            "created_at": None,
        }
        mock_record = MagicMock(**account_record)
        mock_database.fetch_one = AsyncMock(return_value=mock_record)

        result = await account_service.create(account_in)

        assert result.id == account_id
        assert result.user_id == 456
        assert result.balance == 0.01

