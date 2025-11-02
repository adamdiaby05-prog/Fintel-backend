from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, Numeric, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import Base

class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    transaction_type = Column(String(50), nullable=False)  # 'deposit', 'withdrawal', 'transfer'
    amount = Column(Numeric(15, 2), nullable=False)
    currency = Column(String(3), default="XOF")  # Franc CFA
    status = Column(String(20), default="pending")  # 'pending', 'completed', 'failed', 'cancelled'
    description = Column(Text, nullable=True)
    reference = Column(String(100), unique=True, index=True, nullable=True)
    network = Column(String(50), nullable=True)  # 'orange', 'mtn', 'moov', 'wave'
    recipient_phone = Column(String(20), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relation avec l'utilisateur
    user = relationship("User", back_populates="transactions")

class Wallet(Base):
    __tablename__ = "wallets"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, unique=True)
    balance = Column(Numeric(15, 2), default=5000.00)  # Solde par défaut de 5000 XOF pour les tests
    currency = Column(String(3), default="XOF")
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relation avec l'utilisateur
    user = relationship("User", back_populates="wallet")



