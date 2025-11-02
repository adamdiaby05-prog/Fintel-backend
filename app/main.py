from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1 import auth, transactions, user
from app.core.database import engine, Base
from config import settings

# Créer les tables de base de données
Base.metadata.create_all(bind=engine)

# Créer l'application FastAPI
app = FastAPI(
    title=settings.project_name,
    version="1.0.0",
    description="API pour l'application Fintel - Gestion de portefeuille mobile"
)

# Configuration CORS - Autoriser toutes les origines pour le développement mobile
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Autoriser toutes les origines en développement
    allow_credentials=False,  # Doit être False si allow_origins=["*"]
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inclure les routers
app.include_router(
    auth.router,
    prefix=f"{settings.api_v1_str}/auth",
    tags=["Authentication"]
)

app.include_router(
    transactions.router,
    prefix=f"{settings.api_v1_str}/transactions",
    tags=["Transactions"]
)

app.include_router(
    user.router,
    prefix=f"{settings.api_v1_str}/user",
    tags=["User"]
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

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)


