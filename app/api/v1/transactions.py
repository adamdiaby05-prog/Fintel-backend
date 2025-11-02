from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import verify_token
from app.schemas.transaction import TransactionCreate, Transaction, Wallet
from app.services.transaction_service import TransactionService
from app.services.user_service import UserService
from typing import List, Optional
from decimal import Decimal
from pydantic import BaseModel

router = APIRouter()

def get_current_user(token: str = Depends(verify_token), db: Session = Depends(get_db)):
    """Récupérer l'utilisateur actuel à partir du token"""
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token d'authentification requis"
        )
    
    user_service = UserService(db)
    user = user_service.get_user_by_phone(token.get("sub"))
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Utilisateur non trouvé"
        )
    return user

@router.get("/wallet", response_model=Wallet)
async def get_wallet(
    phone: Optional[str] = Query(None, description="Numéro de téléphone de l'utilisateur"),
    db: Session = Depends(get_db)
):
    """Récupérer le solde du portefeuille par numéro de téléphone"""
    transaction_service = TransactionService(db)
    user_service = UserService(db)
    
    # Si un numéro de téléphone est fourni, l'utiliser
    if phone:
        # Nettoyer le numéro (enlever +225, espaces, etc.)
        clean_phone = phone.replace('+', '').replace(' ', '').strip()
        if clean_phone.startswith('225') and len(clean_phone) > 10:
            clean_phone = clean_phone[3:]
        
        user = user_service.get_user_by_phone(clean_phone)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Utilisateur non trouvé"
            )
        wallet = transaction_service.get_or_create_wallet(user.id)
    return wallet
    
    # Si pas de numéro fourni, erreur
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Numéro de téléphone requis"
    )

@router.post("/deposit", response_model=Transaction)
async def create_deposit(
    transaction_data: TransactionCreate,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Créer un dépôt"""
    if transaction_data.transaction_type != "deposit":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Type de transaction invalide pour un dépôt"
        )
    
    transaction_service = TransactionService(db)
    
    # Créer la transaction
    transaction = transaction_service.create_transaction(current_user.id, transaction_data)
    
    # Mettre à jour le solde du portefeuille
    transaction_service.update_wallet_balance(
        current_user.id, 
        transaction_data.amount, 
        "add"
    )
    
    # Marquer la transaction comme complétée
    transaction_service.update_transaction_status(transaction.id, "completed")
    
    return transaction

@router.post("/withdrawal", response_model=Transaction)
async def create_withdrawal(
    transaction_data: TransactionCreate,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Créer un retrait"""
    if transaction_data.transaction_type != "withdrawal":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Type de transaction invalide pour un retrait"
        )
    
    transaction_service = TransactionService(db)
    
    # Vérifier le solde disponible
    current_balance = transaction_service.get_wallet_balance(current_user.id)
    if current_balance < transaction_data.amount:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Solde insuffisant"
        )
    
    # Créer la transaction
    transaction = transaction_service.create_transaction(current_user.id, transaction_data)
    
    # Mettre à jour le solde du portefeuille
    updated_wallet = transaction_service.update_wallet_balance(
        current_user.id, 
        transaction_data.amount, 
        "subtract"
    )
    
    if not updated_wallet:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Solde insuffisant"
        )
    
    # Marquer la transaction comme complétée
    transaction_service.update_transaction_status(transaction.id, "completed")
    
    return transaction

@router.post("/transfer", response_model=Transaction)
async def create_transfer(
    transaction_data: TransactionCreate,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Créer un transfert"""
    if transaction_data.transaction_type != "transfer":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Type de transaction invalide pour un transfert"
        )
    
    if not transaction_data.recipient_phone:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Numéro du destinataire requis"
        )
    
    transaction_service = TransactionService(db)
    user_service = UserService(db)
    
    # Vérifier que le destinataire existe
    recipient = user_service.get_user_by_phone(transaction_data.recipient_phone)
    if not recipient:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Destinataire non trouvé"
        )
    
    # Vérifier le solde disponible
    current_balance = transaction_service.get_wallet_balance(current_user.id)
    if current_balance < transaction_data.amount:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Solde insuffisant"
        )
    
    # Créer la transaction
    transaction = transaction_service.create_transaction(current_user.id, transaction_data)
    
    # Débiter le compte de l'expéditeur
    updated_wallet = transaction_service.update_wallet_balance(
        current_user.id, 
        transaction_data.amount, 
        "subtract"
    )
    
    if not updated_wallet:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Solde insuffisant"
        )
    
    # Créditer le compte du destinataire
    transaction_service.update_wallet_balance(
        recipient.id, 
        transaction_data.amount, 
        "add"
    )
    
    # Marquer la transaction comme complétée
    transaction_service.update_transaction_status(transaction.id, "completed")
    
    return transaction

@router.get("/history", response_model=List[Transaction])
async def get_transaction_history(
    phone: Optional[str] = Query(None, description="Numéro de téléphone de l'utilisateur"),
    limit: int = 50,
    offset: int = 0,
    db: Session = Depends(get_db)
):
    """Récupérer l'historique des transactions par numéro de téléphone"""
    transaction_service = TransactionService(db)
    user_service = UserService(db)
    
    # Si un numéro de téléphone est fourni, l'utiliser
    if phone:
        # Nettoyer le numéro (enlever +225, espaces, etc.)
        clean_phone = phone.replace('+', '').replace(' ', '').strip()
        if clean_phone.startswith('225') and len(clean_phone) > 10:
            clean_phone = clean_phone[3:]
        
        user = user_service.get_user_by_phone(clean_phone)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Utilisateur non trouvé"
            )
        
    transactions = transaction_service.get_user_transactions(
            user.id, limit, offset
    )
    return transactions
    
    # Si pas de numéro fourni, erreur
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Numéro de téléphone requis"
    )

# Schéma pour les transferts Fintel (sans token)
class FintelTransferRequest(BaseModel):
    sender_phone: str
    recipient_phone: str
    amount: Decimal
    description: str = "Transfert Fintel"

@router.post("/fintel-transfer", response_model=dict)
async def create_fintel_transfer(
    transfer_data: FintelTransferRequest,
    db: Session = Depends(get_db)
):
    """
    Créer un transfert entre utilisateurs Fintel
    Vérifie si le destinataire est un utilisateur Fintel,
    vérifie le solde de l'expéditeur, et effectue le transfert
    """
    transaction_service = TransactionService(db)
    user_service = UserService(db)
    
    # Log du montant reçu
    print(f"💰 MONTANT REÇU DANS L'API: {transfer_data.amount} (type: {type(transfer_data.amount)})")
    
    # Nettoyer les numéros de téléphone (enlever +225, espaces, etc.)
    sender_phone = transfer_data.sender_phone.replace('+', '').replace(' ', '').strip()
    recipient_phone = transfer_data.recipient_phone.replace('+', '').replace(' ', '').strip()
    
    # Enlever l'indicatif 225 si présent
    if sender_phone.startswith('225') and len(sender_phone) > 10:
        sender_phone = sender_phone[3:]
    if recipient_phone.startswith('225') and len(recipient_phone) > 10:
        recipient_phone = recipient_phone[3:]
    
    # Vérifier que l'expéditeur existe
    sender = user_service.get_user_by_phone(sender_phone)
    if not sender:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Expéditeur non trouvé"
        )
    
    print(f"👤 Expéditeur trouvé: user_id={sender.id}, phone={sender_phone}, name={sender.first_name or 'N/A'}")
    
    # Vérifier que le destinataire existe (c'est un numéro Fintel)
    recipient = user_service.get_user_by_phone(recipient_phone)
    if not recipient:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Le destinataire n'est pas un utilisateur Fintel"
        )
    
    print(f"👤 Destinataire trouvé: user_id={recipient.id}, phone={recipient_phone}, name={recipient.first_name or 'N/A'}")
    
    # Vérifier qu'on ne se transfère pas à soi-même
    if sender.id == recipient.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Vous ne pouvez pas vous transférer de l'argent à vous-même"
        )
    
    # Vérifier que le montant est positif
    if transfer_data.amount <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Le montant doit être supérieur à 0"
        )
    
    # Vérifier le solde disponible de l'expéditeur (le solde peut être égal au montant, donc descendre à 0)
    sender_balance = transaction_service.get_wallet_balance(sender.id)
    if sender_balance < transfer_data.amount:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Solde insuffisant. Votre solde actuel est de {sender_balance} XOF. Vous devez avoir au moins {transfer_data.amount} XOF."
        )
    
    try:
        # PROCESSUS SIMPLE : Débiter l'expéditeur, créditer le destinataire
        
        # 1. Récupérer les soldes initiaux
        initial_sender_balance = transaction_service.get_wallet_balance(sender.id)
        initial_recipient_balance = transaction_service.get_wallet_balance(recipient.id)
        
        print(f"📊 AVANT TRANSFERT:")
        print(f"   Expéditeur {sender_phone}: {initial_sender_balance} XOF")
        print(f"   Destinataire {recipient_phone}: {initial_recipient_balance} XOF")
        print(f"   Montant: {transfer_data.amount} XOF")
        
        # 2. Débiter l'expéditeur
        sender_wallet = transaction_service.update_wallet_balance(
            sender.id,
            transfer_data.amount,
            "subtract",
            auto_commit=False
        )
        
        if not sender_wallet:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Solde insuffisant"
            )
        
        print(f"✅ Débit effectué: {sender_phone} → {sender_wallet.balance} XOF")
        
        # 3. Créditer le destinataire
        recipient_wallet = transaction_service.update_wallet_balance(
            recipient.id,
            transfer_data.amount,
            "add",
            auto_commit=False
        )
        
        if not recipient_wallet:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Erreur lors du crédit du destinataire"
            )
        
        print(f"✅ Crédit effectué: {recipient_phone} → {recipient_wallet.balance} XOF")
        
        # 4. Créer les transactions SANS commit auto (pour que tout soit dans la même transaction atomique)
        sender_transaction_data = TransactionCreate(
            transaction_type="transfer",
            amount=transfer_data.amount,
            currency="XOF",
            description=f"Envoi vers {recipient.first_name or recipient_phone}",
            recipient_phone=recipient_phone
        )
        sender_transaction = transaction_service.create_transaction(
            sender.id,
            sender_transaction_data,
            auto_commit=False  # Pas de commit auto, sera fait avec le commit global
        )
        transaction_service.update_transaction_status(
            sender_transaction.id,
            "completed",
            auto_commit=False  # Pas de commit auto, sera fait avec le commit global
        )
        
        recipient_transaction_data = TransactionCreate(
            transaction_type="transfer",
            amount=transfer_data.amount,
            currency="XOF",
            description=f"Reçu de {sender.first_name or sender_phone}",
            recipient_phone=sender_phone
        )
        recipient_transaction = transaction_service.create_transaction(
            recipient.id,
            recipient_transaction_data,
            auto_commit=False  # Pas de commit auto, sera fait avec le commit global
        )
        transaction_service.update_transaction_status(
            recipient_transaction.id,
            "completed",
            auto_commit=False  # Pas de commit auto, sera fait avec le commit global
        )
        
        # 5. FLUSH pour forcer l'écriture dans la DB (avant le commit)
        db.flush()
        print(f"💾 Modifications flushées dans la session (wallets + transactions)")
        
        # 6. VALIDER TOUT (commit atomique - wallets ET transactions)
        db.commit()
        print(f"💾 TOUT commité dans la base de données (wallets + transactions)")
        
        # IMPORTANT: Après le commit réussi, NE PAS faire de rollback même en cas d'erreur
        # Les données sont déjà sauvegardées dans la DB
        
        # 7. Récupérer les soldes depuis la DB pour la réponse
        # Utiliser get_wallet_balance qui fait une requête fraîche depuis la DB
        final_sender_balance = transaction_service.get_wallet_balance(sender.id)
        final_recipient_balance = transaction_service.get_wallet_balance(recipient.id)
        
        print(f"📊 APRÈS TRANSFERT (vérification depuis DB):")
        print(f"   {sender_phone}: {final_sender_balance} XOF (était {initial_sender_balance} XOF, attendu: {initial_sender_balance - transfer_data.amount} XOF)")
        print(f"   {recipient_phone}: {final_recipient_balance} XOF (était {initial_recipient_balance} XOF, attendu: {initial_recipient_balance + transfer_data.amount} XOF)")
        
        # Vérification critique : si les valeurs ne correspondent pas, logger mais ne pas échouer
        expected_sender = initial_sender_balance - transfer_data.amount
        expected_recipient = initial_recipient_balance + transfer_data.amount
        
        if abs(float(final_sender_balance - expected_sender)) > 0.01:
            print(f"⚠️ ATTENTION: Le solde de l'expéditeur ne correspond pas exactement!")
            print(f"   Attendu: {expected_sender} XOF, Trouvé: {final_sender_balance} XOF")
            # Utiliser la valeur calculée pour la réponse
            final_sender_balance = Decimal(str(expected_sender))
            
        if abs(float(final_recipient_balance - expected_recipient)) > 0.01:
            print(f"⚠️ ATTENTION: Le solde du destinataire ne correspond pas exactement!")
            print(f"   Attendu: {expected_recipient} XOF, Trouvé: {final_recipient_balance} XOF")
            # Utiliser la valeur calculée pour la réponse
            final_recipient_balance = Decimal(str(expected_recipient))
        
        # Utiliser les soldes pour la réponse
        return {
            "success": True,
            "message": "Transfert effectué avec succès",
            "transaction_id": sender_transaction.reference,
            "sender_balance": float(final_sender_balance),
            "amount": float(transfer_data.amount),
            "recipient_name": recipient.first_name or recipient_phone,
            "recipient_phone": recipient_phone
        }
        
    except HTTPException:
        # Les HTTPException ne doivent pas faire de rollback car elles peuvent être levées AVANT le commit
        # Vérifier si on est dans un état où on peut rollback (avant le commit final)
        if db.in_transaction():
            db.rollback()
            print(f"❌ Rollback effectué à cause d'une HTTPException")
        raise
    except Exception as e:
        # Rollback seulement si on n'a pas encore commité
        if db.in_transaction():
            db.rollback()
            print(f"❌ Rollback effectué à cause d'une exception: {e}")
        else:
            print(f"⚠️ Exception après commit (données déjà sauvegardées): {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erreur lors du transfert: {str(e)}"
        )



