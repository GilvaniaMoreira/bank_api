from enum import Enum

from pydantic import BaseModel, ConfigDict, PositiveFloat


class TransactionType(Enum):
    DEPOSIT = "deposit"
    WITHDRAWAL = "withdrawal"


class TransactionIn(BaseModel):
    model_config = ConfigDict(use_enum_values=True)
    
    account_id: int
    type: TransactionType
    amount: PositiveFloat