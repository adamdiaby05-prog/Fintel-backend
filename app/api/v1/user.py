from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.user import UserUpdate
from app.services.user_service import UserService
from typing import Optional

router = APIRouter()

@router.get("/profile", response_model=dict)
async def get_user_profile(
    phone: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Récupérer le profil d'un utilisateur"""
    user_service = UserService(db)
    
    if not phone:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Le numéro de téléphone est requis"
        )
    
    user = user_service.get_user_by_phone(phone)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Utilisateur non trouvé"
        )
    
    return {
        "user": {
            "id": user.id,
            "phone_number": user.phone_number,
            "whatsapp_number": user.whatsapp_number,
            "email": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "date_of_birth": user.date_of_birth.isoformat() if user.date_of_birth else None,
            "country": user.country,
            "city": user.city,
            "address": user.address,
            "id_type": user.id_type,
            "id_number": user.id_number,
            "id_issue_date": user.id_issue_date.isoformat() if user.id_issue_date else None,
            "id_expiry_date": user.id_expiry_date.isoformat() if user.id_expiry_date else None,
            "profile_picture_url": user.profile_picture_url,
            "front_id_photo_url": user.front_id_photo_url,
            "back_id_photo_url": user.back_id_photo_url,
            "selfie_photo_url": user.selfie_photo_url,
            "otp_delivery_preference": user.otp_delivery_preference,
            "terms_accepted": user.terms_accepted,
            "privacy_policy_accepted": user.privacy_policy_accepted,
            "is_active": user.is_active,
            "is_verified": user.is_verified,
            "created_at": user.created_at.isoformat() if user.created_at else None,
            "updated_at": user.updated_at.isoformat() if user.updated_at else None,
        }
    }

@router.put("/profile", response_model=dict)
async def update_user_profile(
    user_update: UserUpdate,
    phone: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Mettre à jour le profil d'un utilisateur (ou créer si n'existe pas)"""
    user_service = UserService(db)
    
    # Utiliser le phone_number du body ou du query parameter
    phone_to_use = user_update.phone_number or phone
    if not phone_to_use:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Le numéro de téléphone est requis"
        )
    
    user = user_service.get_user_by_phone(phone_to_use)
    
    # Si l'utilisateur n'existe pas, le créer d'abord
    if not user:
        from app.schemas.user import UserCreate
        try:
            # Créer un nouvel utilisateur avec juste le numéro de téléphone
            user_create = UserCreate(
                phone_number=phone_to_use,
                password=None  # Le mot de passe sera mis à jour plus tard
            )
            user = user_service.create_user(user_create)
            print(f"✅ Nouvel utilisateur créé avec phone_number: {phone_to_use}")
        except Exception as e:
            print(f"❌ Erreur lors de la création de l'utilisateur: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Erreur lors de la création de l'utilisateur: {str(e)}"
            )
    
    # Mettre à jour l'utilisateur
    updated_user = user_service.update_user(user.id, user_update)
    
    if not updated_user:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erreur lors de la mise à jour du profil"
        )
    
    return {
        "message": "Profil mis à jour avec succès",
        "success": True,
        "user": {
            "id": updated_user.id,
            "phone_number": updated_user.phone_number,
            "whatsapp_number": updated_user.whatsapp_number,
            "email": updated_user.email,
            "first_name": updated_user.first_name,
            "last_name": updated_user.last_name,
            "date_of_birth": updated_user.date_of_birth.isoformat() if updated_user.date_of_birth else None,
            "country": updated_user.country,
            "city": updated_user.city,
            "address": updated_user.address,
            "id_type": updated_user.id_type,
            "id_number": updated_user.id_number,
            "id_issue_date": updated_user.id_issue_date.isoformat() if updated_user.id_issue_date else None,
            "id_expiry_date": updated_user.id_expiry_date.isoformat() if updated_user.id_expiry_date else None,
            "profile_picture_url": updated_user.profile_picture_url,
            "is_verified": updated_user.is_verified,
        }
    }

