from typing import Union

from pydantic import AwareDatetime, BaseModel, NaiveDatetime, PositiveFloat


class AccountOut(BaseModel):
    id: int
    user_id: int
    balance: float
    created_at: Union[AwareDatetime, NaiveDatetime]


class TransactionOut(BaseModel):
    id: int
    account_id: int
    type: str
    amount: PositiveFloat
    timestamp: Union[AwareDatetime, NaiveDatetime]