"""Testes para as exceções customizadas."""
import pytest

from src.exceptions import (
    AccountNotFoundError,
    BusinessError,
    InsufficientBalanceError,
    InvalidAmountError,
    InvalidTransactionError,
    TransactionNotFoundError,
)


class TestAccountNotFoundError:
    """Testes para AccountNotFoundError."""

    def test_account_not_found_error_without_id(self):
        """Testa AccountNotFoundError sem ID."""
        error = AccountNotFoundError()
        assert str(error) == "Account not found."
        assert error.message == "Account not found."

    def test_account_not_found_error_with_id(self):
        """Testa AccountNotFoundError com ID."""
        error = AccountNotFoundError(account_id=123)
        assert str(error) == "Account with ID 123 not found."
        assert error.message == "Account with ID 123 not found."


class TestTransactionNotFoundError:
    """Testes para TransactionNotFoundError."""

    def test_transaction_not_found_error_without_id(self):
        """Testa TransactionNotFoundError sem ID."""
        error = TransactionNotFoundError()
        assert str(error) == "Transaction not found."
        assert error.message == "Transaction not found."

    def test_transaction_not_found_error_with_id(self):
        """Testa TransactionNotFoundError com ID."""
        error = TransactionNotFoundError(transaction_id=456)
        assert str(error) == "Transaction with ID 456 not found."
        assert error.message == "Transaction with ID 456 not found."


class TestBusinessError:
    """Testes para BusinessError."""

    def test_business_error_default_message(self):
        """Testa BusinessError com mensagem padrão."""
        error = BusinessError()
        assert str(error) == "Business rule violation."
        assert error.message == "Business rule violation."

    def test_business_error_custom_message(self):
        """Testa BusinessError com mensagem customizada."""
        error = BusinessError("Custom business error")
        assert str(error) == "Custom business error"
        assert error.message == "Custom business error"


class TestInsufficientBalanceError:
    """Testes para InsufficientBalanceError."""

    def test_insufficient_balance_error_default(self):
        """Testa InsufficientBalanceError sem parâmetros."""
        error = InsufficientBalanceError()
        assert str(error) == "Operation not carried out due to lack of balance."
        assert error.message == "Operation not carried out due to lack of balance."

    def test_insufficient_balance_error_with_account_id(self):
        """Testa InsufficientBalanceError com account_id."""
        error = InsufficientBalanceError(account_id=123)
        assert str(error) == "Insufficient balance for account 123."
        assert error.message == "Insufficient balance for account 123."

    def test_insufficient_balance_error_with_account_id_and_balance(self):
        """Testa InsufficientBalanceError com account_id e balance."""
        error = InsufficientBalanceError(account_id=123, balance=50.50)
        assert str(error) == "Insufficient balance for account 123. Current balance: 50.50."
        assert error.message == "Insufficient balance for account 123. Current balance: 50.50."

    def test_insufficient_balance_error_inherits_from_business_error(self):
        """Testa que InsufficientBalanceError herda de BusinessError."""
        error = InsufficientBalanceError()
        assert isinstance(error, BusinessError)


class TestInvalidAmountError:
    """Testes para InvalidAmountError."""

    def test_invalid_amount_error_default(self):
        """Testa InvalidAmountError sem parâmetros."""
        error = InvalidAmountError()
        assert str(error) == "Invalid transaction amount. Amount must be greater than zero."
        assert error.message == "Invalid transaction amount. Amount must be greater than zero."

    def test_invalid_amount_error_with_amount(self):
        """Testa InvalidAmountError com amount."""
        error = InvalidAmountError(amount=-10.0)
        assert str(error) == "Invalid amount: -10.00. Amount must be greater than zero."
        assert error.message == "Invalid amount: -10.00. Amount must be greater than zero."

    def test_invalid_amount_error_with_reason(self):
        """Testa InvalidAmountError com reason."""
        error = InvalidAmountError(reason="Amount exceeds maximum limit")
        assert str(error) == "Invalid amount: Amount exceeds maximum limit."
        assert error.message == "Invalid amount: Amount exceeds maximum limit."

    def test_invalid_amount_error_with_amount_and_reason(self):
        """Testa InvalidAmountError com amount e reason."""
        error = InvalidAmountError(amount=1000.0, reason="Amount exceeds maximum limit")
        assert str(error) == "Invalid amount 1000.00: Amount exceeds maximum limit."
        assert error.message == "Invalid amount 1000.00: Amount exceeds maximum limit."


class TestInvalidTransactionError:
    """Testes para InvalidTransactionError."""

    def test_invalid_transaction_error_default(self):
        """Testa InvalidTransactionError com mensagem padrão."""
        error = InvalidTransactionError()
        assert str(error) == "Invalid transaction."
        assert error.message == "Invalid transaction."

    def test_invalid_transaction_error_custom_message(self):
        """Testa InvalidTransactionError com mensagem customizada."""
        error = InvalidTransactionError("Transaction is invalid for this account type")
        assert str(error) == "Transaction is invalid for this account type"
        assert error.message == "Transaction is invalid for this account type"


