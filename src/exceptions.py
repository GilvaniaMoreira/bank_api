from typing import Optional


class AccountNotFoundError(Exception):
    def __init__(self, account_id: Optional[int] = None):
        self.account_id = account_id
        if account_id:
            self.message = f"Account with ID {account_id} not found."
        else:
            self.message = "Account not found."
        super().__init__(self.message)


class TransactionNotFoundError(Exception):
    def __init__(self, transaction_id: Optional[int] = None):
        if transaction_id:
            self.message = f"Transaction with ID {transaction_id} not found."
        else:
            self.message = "Transaction not found."
        super().__init__(self.message)


class BusinessError(Exception):
    def __init__(self, message: str = "Business rule violation."):
        self.message = message
        super().__init__(self.message)


class InsufficientBalanceError(BusinessError):
    def __init__(self, account_id: Optional[int] = None, balance: Optional[float] = None):
        self.account_id = account_id
        self.balance = balance
        if account_id and balance is not None:
            self.message = f"Insufficient balance for account {account_id}. Current balance: {balance:.2f}."
        elif account_id:
            self.message = f"Insufficient balance for account {account_id}."
        else:
            self.message = "Operation not carried out due to lack of balance."
        super().__init__(self.message)


class InvalidAmountError(BusinessError):
    def __init__(self, amount: Optional[float] = None, reason: Optional[str] = None):
        if amount is not None and reason:
            self.message = f"Invalid amount {amount:.2f}: {reason}."
        elif amount is not None:
            self.message = f"Invalid amount: {amount:.2f}. Amount must be greater than zero."
        elif reason:
            self.message = f"Invalid amount: {reason}."
        else:
            self.message = "Invalid transaction amount. Amount must be greater than zero."
        super().__init__(self.message)


class InvalidTransactionError(BusinessError):
    def __init__(self, message: str = "Invalid transaction."):
        self.message = message
        super().__init__(self.message)