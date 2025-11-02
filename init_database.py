#!/usr/bin/env python3
"""
Script d'initialisation de la base de données
Ce script crée toutes les tables nécessaires pour l'application Fintel
"""

import sys
import os

# Ajouter le répertoire parent au path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.core.database import Base, engine
# Importer les modèles pour qu'ils soient enregistrés dans Base.metadata
from app.models.user import User, OTP
from app.models.transaction import Transaction, Wallet

def init_database():
    """Créer toutes les tables dans la base de données"""
    try:
        print("🔄 Création des tables dans la base de données...")
        print(f"📊 Connexion à: {engine.url}")
        
        # Créer toutes les tables
        Base.metadata.create_all(bind=engine)
        
        print("✅ Toutes les tables ont été créées avec succès!")
        print("\n📊 Tables créées:")
        print("   ✅ users")
        print("   ✅ otps")
        print("   ✅ wallets")
        print("   ✅ transactions")
        
        return True
    except Exception as e:
        print(f"❌ Erreur lors de la création des tables: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = init_database()
    sys.exit(0 if success else 1)
