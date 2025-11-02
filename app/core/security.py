from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
import bcrypt
from config import settings
import random
import string

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Vérifier un mot de passe (compatible avec bcrypt et passlib)"""
    try:
        if not plain_password or not hashed_password:
            return False
        
        # Convertir le mot de passe en bytes si nécessaire
        if isinstance(plain_password, str):
            plain_password_bytes = plain_password.encode('utf-8')
        else:
            plain_password_bytes = plain_password
        
        # Le hash peut être en string (bcrypt standard) ou bytes
        if isinstance(hashed_password, str):
            hashed_password_bytes = hashed_password.encode('utf-8')
        else:
            hashed_password_bytes = hashed_password
        
        # Vérifier avec bcrypt (compatible avec passlib qui utilise aussi bcrypt)
        return bcrypt.checkpw(plain_password_bytes, hashed_password_bytes)
    except Exception as e:
        print(f"Erreur lors de la vérification du mot de passe: {e}")
        return False

def get_password_hash(password: str) -> str:
    """Hacher un mot de passe avec bcrypt"""
    # Bcrypt a une limite de 72 bytes pour le mot de passe en clair
    # Convertir en bytes et tronquer si nécessaire
    if isinstance(password, str):
        password_bytes = password.encode('utf-8')
        if len(password_bytes) > 72:
            password_bytes = password_bytes[:72]
        # Générer le salt et hasher
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password_bytes, salt)
        return hashed.decode('utf-8')
    else:
        # Si c'est déjà en bytes
        if len(password) > 72:
            password = password[:72]
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password, salt)
        return hashed.decode('utf-8')

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """Créer un token JWT"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.access_token_expire_minutes)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)
    return encoded_jwt

def verify_token(token: str) -> Optional[dict]:
    """Vérifier un token JWT"""
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
        return payload
    except JWTError:
        return None

def generate_otp(length: int = None) -> str:
    """Générer un code OTP"""
    if length is None:
        length = settings.otp_length
    return ''.join(random.choices(string.digits, k=length))

def is_otp_expired(created_at: datetime) -> bool:
    """Vérifier si un OTP a expiré"""
    expire_time = created_at + timedelta(minutes=settings.otp_expire_minutes)
    return datetime.utcnow() > expire_time


