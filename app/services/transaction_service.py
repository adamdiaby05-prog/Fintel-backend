from sqlalchemy.orm import Session
from sqlalchemy import and_
from app.models.transaction import Transaction, Wallet
from app.schemas.transaction import TransactionCreate, TransactionUpdate
from decimal import Decimal
from typing import Optional, List
import uuid

class TransactionService:
    def __init__(self, db: Session):
        self.db = db

    def create_transaction(self, user_id: int, transaction_data: TransactionCreate, auto_commit: bool = True) -> Transaction:
        """Créer une nouvelle transaction
        
        Args:
            user_id: ID de l'utilisateur
            transaction_data: Données de la transaction
            auto_commit: Si True, commit automatiquement. Si False, laisse le commit à l'appelant (pour transactions atomiques)
        """
        # Générer une référence unique
        reference = f"TXN_{uuid.uuid4().hex[:12].upper()}"
        
        # Utiliser model_dump pour Pydantic v2 ou dict pour v1
        try:
            transaction_dict = transaction_data.model_dump()
        except AttributeError:
            transaction_dict = transaction_data.dict()
        
        db_transaction = Transaction(
            user_id=user_id,
            reference=reference,
            **transaction_dict
        )
        
        self.db.add(db_transaction)
        
        if auto_commit:
            self.db.commit()
            self.db.refresh(db_transaction)
        # Si auto_commit=False, le commit sera fait par l'appelant
        
        return db_transaction

    def get_transaction_by_id(self, transaction_id: int) -> Optional[Transaction]:
        """Récupérer une transaction par ID"""
        return self.db.query(Transaction).filter(Transaction.id == transaction_id).first()

    def get_user_transactions(self, user_id: int, limit: int = 50, offset: int = 0) -> List[Transaction]:
        """Récupérer les transactions d'un utilisateur"""
        return self.db.query(Transaction).filter(
            Transaction.user_id == user_id
        ).order_by(Transaction.created_at.desc()).offset(offset).limit(limit).all()

    def update_transaction_status(self, transaction_id: int, status: str, reference: str = None, auto_commit: bool = True) -> Optional[Transaction]:
        """Mettre à jour le statut d'une transaction
        
        Args:
            transaction_id: ID de la transaction
            status: Nouveau statut
            reference: Nouvelle référence (optionnel)
            auto_commit: Si True, commit automatiquement. Si False, laisse le commit à l'appelant (pour transactions atomiques)
        """
        db_transaction = self.get_transaction_by_id(transaction_id)
        if not db_transaction:
            return None
        
        db_transaction.status = status
        if reference:
            db_transaction.reference = reference
        
        if auto_commit:
            self.db.commit()
            self.db.refresh(db_transaction)
        # Si auto_commit=False, le commit sera fait par l'appelant
        
        return db_transaction

    def get_or_create_wallet(self, user_id: int) -> Wallet:
        """Récupérer ou créer un portefeuille pour un utilisateur"""
        # Utiliser une requête simple sans expire_all pour éviter d'annuler les changements en cours
        wallet = self.db.query(Wallet).filter(Wallet.user_id == user_id).first()
        if not wallet:
            # Créer un wallet avec un solde initial de 5000 XOF pour les tests
            wallet = Wallet(user_id=user_id, balance=Decimal('5000.00'))
            self.db.add(wallet)
            self.db.commit()
            self.db.refresh(wallet)
            print(f"📦 Nouveau wallet créé pour user_id={user_id} avec solde initial de 5000 XOF")
        else:
            # Wallet existant trouvé, ne pas faire de refresh car cela peut annuler les changements en cours
            print(f"📦 Wallet existant trouvé pour user_id={user_id}, solde actuel: {wallet.balance} XOF, wallet.id={wallet.id}")
        return wallet

    def update_wallet_balance(self, user_id: int, amount: Decimal, operation: str = "add", auto_commit: bool = False) -> Optional[Wallet]:
        """Mettre à jour le solde du portefeuille
        
        Args:
            user_id: ID de l'utilisateur
            amount: Montant à ajouter ou soustraire
            operation: "add" pour ajouter, "subtract" pour soustraire
            auto_commit: Si True, commit automatiquement. Si False, laisse le commit à l'appelant (pour transactions atomiques)
        """
        # Utiliser with_for_update pour verrouiller le wallet pendant la transaction
        # Cela garantit qu'aucune autre transaction ne peut le modifier en même temps
        from sqlalchemy import select
        wallet_query = select(Wallet).filter(Wallet.user_id == user_id).with_for_update()
        wallet = self.db.execute(wallet_query).scalar_one_or_none()
        
        # Si le wallet n'existe pas, le créer
        if not wallet:
            wallet = Wallet(user_id=user_id, balance=Decimal('5000.00'))
            self.db.add(wallet)
            # Flush pour obtenir l'ID du wallet créé
            self.db.flush()
            print(f"📦 Nouveau wallet créé pour user_id={user_id} avec solde initial de 5000 XOF")
        
        # Vérifier que le wallet appartient bien au bon utilisateur
        if wallet.user_id != user_id:
            print(f"❌ ERREUR CRITIQUE: Le wallet.id={wallet.id} appartient à user_id={wallet.user_id} mais on essaie de modifier pour user_id={user_id}")
            raise ValueError(f"Wallet mismatch: wallet.user_id={wallet.user_id} != user_id={user_id}")
        
        old_balance = wallet.balance
        print(f"📦 Wallet trouvé: wallet.id={wallet.id}, user_id={wallet.user_id}, solde actuel: {wallet.balance} XOF")
        print(f"🔍 update_wallet_balance: user_id={user_id}, wallet.id={wallet.id}, wallet.user_id={wallet.user_id}, operation={operation}, amount={amount}, old_balance={old_balance}")
        
        # Valider que l'opération est correcte
        if operation not in ["add", "subtract"]:
            raise ValueError(f"Opération invalide: {operation}. Utilisez 'add' ou 'subtract'")
        
        # Effectuer l'opération
        if operation == "add":
            new_balance = old_balance + amount
            wallet.balance = new_balance
            # Forcer la mise à jour de updated_at manuellement
            from datetime import datetime, timezone
            wallet.updated_at = datetime.now(timezone.utc)
            print(f"✅ Ajout: User {user_id} (wallet.id={wallet.id}) - Ancien solde: {old_balance} XOF + {amount} XOF = Nouveau solde: {new_balance} XOF")
        elif operation == "subtract":
            # Le solde peut descendre à 0, mais pas en dessous
            if wallet.balance >= amount:
                new_balance = old_balance - amount
                wallet.balance = new_balance
                # Forcer la mise à jour de updated_at manuellement
                from datetime import datetime, timezone
                wallet.updated_at = datetime.now(timezone.utc)
                print(f"✅ Débit: User {user_id} (wallet.id={wallet.id}) - Ancien solde: {old_balance} XOF - {amount} XOF = Nouveau solde: {new_balance} XOF")
            else:
                print(f"❌ Solde insuffisant: User {user_id} - Solde actuel: {wallet.balance} XOF < Montant demandé: {amount} XOF")
                return None  # Solde insuffisant
        
        # Le wallet est déjà dans la session (récupéré via query ou créé)
        # Les modifications de balance et updated_at seront automatiquement détectées par SQLAlchemy
        
        # Commit seulement si auto_commit est True
        if auto_commit:
            self.db.commit()
            self.db.refresh(wallet)
        
        print(f"💾 Solde mis à jour en mémoire: wallet.id={wallet.id}, user_id={wallet.user_id}, balance={wallet.balance} XOF, updated_at={wallet.updated_at} (commit: {'oui' if auto_commit else 'non'})")
        return wallet

    def get_wallet_balance(self, user_id: int) -> Decimal:
        """Récupérer le solde du portefeuille"""
        # Expirer le cache pour s'assurer d'avoir la valeur la plus récente
        self.db.expire_all()
        wallet = self.get_or_create_wallet(user_id)
        # Rafraîchir depuis la base de données
        self.db.refresh(wallet)
        return wallet.balance



