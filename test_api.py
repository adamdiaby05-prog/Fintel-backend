from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Créer l'application FastAPI
app = FastAPI(
    title="Fintel API Test",
    version="1.0.0",
    description="API de test pour Fintel"
)

# Configuration CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    """Point d'entrée de l'API"""
    return {
        "message": "Bienvenue sur l'API Fintel",
        "version": "1.0.0",
        "docs": "/docs"
    }

@app.get("/health")
async def health_check():
    """Vérification de l'état de l'API"""
    return {"status": "healthy", "message": "API Fintel opérationnelle"}

@app.post("/api/v1/auth/register")
async def register(phone_number: str):
    """Endpoint de test pour l'enregistrement"""
    return {
        "message": "Utilisateur enregistré avec succès",
        "phone_number": phone_number,
        "otp_code": "1234"
    }

@app.post("/api/v1/auth/verify-otp")
async def verify_otp(phone_number: str, otp_code: str):
    """Endpoint de test pour la vérification OTP"""
    if otp_code == "1234":
        return {
            "message": "OTP vérifié avec succès",
            "phone_number": phone_number,
            "verified": True
        }
    else:
        return {
            "message": "Code OTP incorrect",
            "verified": False
        }

@app.post("/api/v1/auth/login")
async def login(phone_number: str, password: str):
    """Endpoint de test pour la connexion"""
    if password == "azerty":
        return {
            "message": "Connexion réussie",
            "phone_number": phone_number,
            "access_token": "test-token-12345"
        }
    else:
        return {
            "message": "Mot de passe incorrect",
            "verified": False
        }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

