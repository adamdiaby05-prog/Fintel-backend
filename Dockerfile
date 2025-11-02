FROM python:3.11-slim

# Définir le répertoire de travail
WORKDIR /app

# Installer les dépendances système si nécessaire
RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Copier le fichier requirements
COPY requirements.txt .

# Installer les dépendances Python
RUN pip install --no-cache-dir -r requirements.txt

# Copier le code de l'application
COPY . .

# Rendre le script exécutable
RUN chmod +x create_tables.sh || true

# Exposer le port
EXPOSE 8000

# Script de démarrage qui crée les tables puis démarre l'application
CMD ["sh", "-c", "python -c 'from app.core.database import Base, engine; from app.models.user import User, OTP; from app.models.transaction import Transaction, Wallet; Base.metadata.create_all(bind=engine); print(\"✅ Tables créées\")' && uvicorn app.main:app --host 0.0.0.0 --port 8000"]

