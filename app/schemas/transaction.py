from pydantic import BaseModel, field_serializer
from typing import Optional
from datetime import datetime
from decimal import Decimal

class TransactionBase(BaseModel):
    transaction_type: str  # 'deposit', 'withdrawal', 'transfer'
    amount: Decimal
    currency: str = "XOF"
    description: Optional[str] = None
    network: Optional[str] = None
    recipient_phone: Optional[str] = None
    
    @field_serializer('amount')
    def serialize_amount(self, value: Decimal) -> float:
        """Convertir Decimal en float pour la sérialisation JSON"""
        return float(value)

class TransactionCreate(TransactionBase):
    pass

class TransactionUpdate(BaseModel):
    status: Optional[str] = None
    reference: Optional[str] = None

class TransactionInDB(TransactionBase):
    id: int
    user_id: int
    status: str
    reference: Optional[str] = None
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class Transaction(TransactionInDB):
    pass

class WalletBase(BaseModel):
    balance: Decimal
    currency: str = "XOF"
    
    @field_serializer('balance')
    def serialize_balance(self, value: Decimal) -> float:
        """Convertir Decimal en float pour la sérialisation JSON"""
        return float(value)

class WalletInDB(WalletBase):
    id: int
    user_id: int
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class Wallet(WalletInDB):
    pass



