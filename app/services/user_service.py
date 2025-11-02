from sqlalchemy.orm import Session
from sqlalchemy import and_
from app.models.user import User, OTP
from app.schemas.user import UserCreate, UserUpdate
from app.core.security import get_password_hash, verify_password, generate_otp
from datetime import datetime, timedelta
from config import settings
from typing import Optional

class UserService:
    def __init__(self, db: Session):
        self.db = db

    def get_user_by_phone(self, phone_number: str) -> Optional[User]:
        """Récupérer un utilisateur par numéro de téléphone"""
        if not phone_number or not phone_number.strip():
            return None
        return self.db.query(User).filter(User.phone_number == phone_number.strip()).first()

    def get_user_by_id(self, user_id: int) -> Optional[User]:
        """Récupérer un utilisateur par ID"""
        return self.db.query(User).filter(User.id == user_id).first()

    def create_user(self, user_data: UserCreate) -> User:
        """Créer un nouvel utilisateur"""
        try:
            # Valider que le phone_number est fourni
            if not user_data.phone_number or not user_data.phone_number.strip():
                raise ValueError("Le numéro de téléphone est obligatoire")
            
            # Nettoyer et valider les données
            phone_number = user_data.phone_number.strip()
            
            hashed_password = None
            if user_data.password:
                hashed_password = get_password_hash(user_data.password)
            
            db_user = User(
                phone_number=phone_number,
                email=user_data.email.strip() if user_data.email else None,
                first_name=user_data.first_name.strip() if user_data.first_name else None,
                last_name=user_data.last_name.strip() if user_data.last_name else None,
                hashed_password=hashed_password,
                is_verified=False
            )
            
            self.db.add(db_user)
            self.db.commit()
            self.db.refresh(db_user)
            return db_user
        except Exception as e:
            self.db.rollback()
            raise

    def update_user(self, user_id: int, user_data: UserUpdate) -> Optional[User]:
        """Mettre à jour un utilisateur"""
        db_user = self.get_user_by_id(user_id)
        if not db_user:
            return None
        
        # Utiliser model_dump pour Pydantic v2 ou dict pour v1
        try:
            update_data = user_data.model_dump(exclude_unset=True)
        except AttributeError:
            update_data = user_data.dict(exclude_unset=True)
        
        if "password" in update_data and update_data["password"]:
            update_data["hashed_password"] = get_password_hash(update_data.pop("password"))
        
        # Mettre à jour updated_at
        from datetime import datetime
        from sqlalchemy.sql import func
        update_data["updated_at"] = datetime.utcnow()
        
        for field, value in update_data.items():
            if hasattr(db_user, field):
                setattr(db_user, field, value)
        
        self.db.commit()
        self.db.refresh(db_user)
        return db_user

    def verify_password(self, user: User, password: str) -> bool:
        """Vérifier le mot de passe d'un utilisateur"""
        if not user.hashed_password:
            return False
        return verify_password(password, user.hashed_password)

    def create_otp(self, phone_number: str) -> OTP:
        """Créer un code OTP pour un numéro de téléphone"""
        # Supprimer les anciens OTP non utilisés pour ce numéro
        self.db.query(OTP).filter(
            and_(
                OTP.phone_number == phone_number,
                OTP.is_used == False
            )
        ).delete()
        
        # Générer un nouveau OTP
        otp_code = generate_otp()
        expires_at = datetime.utcnow() + timedelta(minutes=settings.otp_expire_minutes)
        
        db_otp = OTP(
            phone_number=phone_number,
            otp_code=otp_code,
            expires_at=expires_at
        )
        
        self.db.add(db_otp)
        self.db.commit()
        self.db.refresh(db_otp)
        return db_otp

    def verify_otp(self, phone_number: str, otp_code: str) -> bool:
        """Vérifier un code OTP"""
        db_otp = self.db.query(OTP).filter(
            and_(
                OTP.phone_number == phone_number,
                OTP.otp_code == otp_code,
                OTP.is_used == False,
                OTP.expires_at > datetime.utcnow()
            )
        ).first()
        
        if db_otp:
            db_otp.is_used = True
            self.db.commit()
            return True
        return False

    def mark_user_verified(self, phone_number: str) -> Optional[User]:
        """Marquer un utilisateur comme vérifié"""
        user = self.get_user_by_phone(phone_number)
        if user:
            user.is_verified = True
            self.db.commit()
            self.db.refresh(user)
        return user



