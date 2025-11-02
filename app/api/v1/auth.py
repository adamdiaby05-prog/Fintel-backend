from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.core.database import get_db
from app.core.security import create_access_token, verify_token
from app.schemas.user import OTPRequest, OTPVerify, UserCreate, UserLogin, Token
from app.services.user_service import UserService
from datetime import timedelta
from config import settings

router = APIRouter()

@router.post("/request-otp", response_model=dict)
async def request_otp(otp_request: OTPRequest, db: Session = Depends(get_db)):
    """Demander un code OTP pour un numéro de téléphone"""
    user_service = UserService(db)
    
    # Pour le numéro de test, retourner toujours le même OTP
    if otp_request.phone_number == "0505979884":
        return {
            "message": "Code OTP envoyé",
            "otp_code": "1234",  # Code de test
            "expires_in_minutes": settings.otp_expire_minutes
        }
    
    # Créer un OTP pour les autres numéros
    otp = user_service.create_otp(otp_request.phone_number)
    
    # En production, ici vous enverriez le SMS
    # Pour le développement, on retourne le code
    return {
        "message": "Code OTP envoyé",
        "otp_code": otp.otp_code,  # À supprimer en production
        "expires_in_minutes": settings.otp_expire_minutes
    }

@router.post("/verify-otp", response_model=dict)
async def verify_otp(otp_verify: OTPVerify, db: Session = Depends(get_db)):
    """Vérifier un code OTP"""
    user_service = UserService(db)
    
    # Autoriser n'importe quel numéro à utiliser '1234' comme OTP (dev/demo)
    if otp_verify.otp_code == "1234":
        user = user_service.get_user_by_phone(otp_verify.phone_number)
        if not user:
            user_data = UserCreate(
                phone_number=otp_verify.phone_number,
                password=otp_verify.password or 'azerty'
            )
            user = user_service.create_user(user_data)
        else:
            # Mettre à jour le mot de passe si fourni
            if otp_verify.password:
                from app.schemas.user import UserUpdate
                user_service.update_user(user.id, UserUpdate(password=otp_verify.password))
        user_service.mark_user_verified(otp_verify.phone_number)
        access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
        access_token = create_access_token(
            data={"sub": user.phone_number}, expires_delta=access_token_expires
        )
        return {
            "message": "OTP vérifié avec succès",
            "access_token": access_token,
            "token_type": "bearer",
            "user": {
                "id": user.id,
                "phone_number": user.phone_number,
                "is_verified": user.is_verified
            }
        }
    
    # Vérifier l'OTP pour les autres numéros
    if user_service.verify_otp(otp_verify.phone_number, otp_verify.otp_code):
        user = user_service.get_user_by_phone(otp_verify.phone_number)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Utilisateur non trouvé"
            )
        user_service.mark_user_verified(otp_verify.phone_number)
        access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
        access_token = create_access_token(
            data={"sub": user.phone_number}, expires_delta=access_token_expires
        )
        return {
            "message": "OTP vérifié avec succès",
            "access_token": access_token,
            "token_type": "bearer",
            "user": {
                "id": user.id,
                "phone_number": user.phone_number,
                "is_verified": user.is_verified
            }
        }
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Code OTP invalide ou expiré"
        )

@router.post("/register", response_model=dict)
async def register(user_data: UserCreate, db: Session = Depends(get_db)):
    """Enregistrer un nouvel utilisateur"""
    try:
        # Valider le numéro de téléphone
        if not user_data.phone_number or not user_data.phone_number.strip():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Le numéro de téléphone est obligatoire"
            )
        
        # Nettoyer le numéro de téléphone (enlever les espaces)
        phone_number = user_data.phone_number.strip()
        
        if not user_data.password or len(user_data.password) < 6:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Le mot de passe est obligatoire et doit faire au moins 6 caractères"
            )
        
        user_service = UserService(db)
        
        # Vérifier si l'utilisateur existe déjà
        existing_user = user_service.get_user_by_phone(phone_number)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Un utilisateur avec ce numéro de téléphone existe déjà"
            )
        
        # Mettre à jour le phone_number dans user_data
        user_data.phone_number = phone_number
        
        # Créer l'utilisateur
        user = user_service.create_user(user_data)
        
        return {
            "message": "Utilisateur créé avec succès",
            "user": {
                "id": user.id,
                "phone_number": user.phone_number,
                "is_verified": user.is_verified
            }
        }
    except HTTPException:
        raise
    except IntegrityError as e:
        db.rollback()
        error_msg = str(e.orig) if hasattr(e, 'orig') else str(e)
        if "phone_number" in error_msg.lower() or "unique" in error_msg.lower():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Un utilisateur avec ce numéro de téléphone existe déjà"
            )
        elif "email" in error_msg.lower() and "unique" in error_msg.lower():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Un utilisateur avec cet email existe déjà"
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Erreur de contrainte de base de données: {error_msg}"
            )
    except Exception as e:
        import traceback
        print(f"Erreur lors de l'inscription: {str(e)}")
        print(traceback.format_exc())
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erreur lors de la création de l'utilisateur: {str(e)}"
        )

@router.post("/login", response_model=Token)
async def login(user_login: UserLogin, db: Session = Depends(get_db)):
    """Connexion avec numéro de téléphone et mot de passe"""
    try:
        user_service = UserService(db)
        
        # Vérifier l'utilisateur
        user = user_service.get_user_by_phone(user_login.phone_number)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Numéro de téléphone ou mot de passe incorrect"
            )
        
        # Vérifier le mot de passe
        if not user.hashed_password:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Aucun mot de passe défini pour ce compte. Veuillez vous réinscrire."
            )
        
        if not user_service.verify_password(user, user_login.password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Numéro de téléphone ou mot de passe incorrect"
            )
        
        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Compte utilisateur désactivé"
            )
        
        # Créer un token d'accès
        access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
        access_token = create_access_token(
            data={"sub": user.phone_number}, expires_delta=access_token_expires
        )
        
        return {
            "access_token": access_token,
            "token_type": "bearer"
        }
    except HTTPException:
        raise
    except Exception as e:
        import traceback
        print(f"Erreur lors de la connexion: {str(e)}")
        print(traceback.format_exc())
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erreur lors de la connexion: {str(e)}"
        )



