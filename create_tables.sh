#!/bin/bash
# Script pour créer les tables au démarrage du conteneur

echo "🔄 Création des tables dans la base de données..."

python -c "
import sys
sys.path.insert(0, '/app')

from app.core.database import Base, engine
from app.models.user import User, OTP
from app.models.transaction import Transaction, Wallet

try:
    print('📊 Connexion à la base de données...')
    Base.metadata.create_all(bind=engine)
    print('✅ Toutes les tables ont été créées avec succès!')
    print('📊 Tables créées: users, otps, wallets, transactions')
except Exception as e:
    print(f'❌ Erreur: {e}')
    import traceback
    traceback.print_exc()
    sys.exit(1)
"

