from pydantic_settings import BaseSettings
from typing import List
import os

class Settings(BaseSettings):
    # Database Configuration
    # Pour déployer ailleurs : utiliser une variable d'environnement DATABASE_URL
    database_url: str = "postgresql://postgres:0000@localhost:5432/fintel"
    db_host: str = "localhost"
    db_port: int = 5432
    db_name: str = "fintel"
    db_user: str = "postgres"
    db_password: str = "0000"
    
    # JWT Configuration
    secret_key: str = "your-secret-key-here-change-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    
    # OTP Configuration
    otp_expire_minutes: int = 5
    otp_length: int = 4
    
    # API Configuration
    api_v1_str: str = "/api/v1"
    project_name: str = "Fintel API"
    
    # CORS Configuration - Autoriser toutes les origines pour le développement mobile
    backend_cors_origins: List[str] = ["*"]
    
    class Config:
        # env_file = ".env"
        case_sensitive = False
        extra = "ignore"

settings = Settings()


