# Fintel Backend API

API FastAPI pour l'application Fintel - Gestion de portefeuille mobile.

## 🚀 Installation et Configuration

### Prérequis
- Python 3.8+
- Docker et Docker Compose
- PostgreSQL (via Docker)

### 1. Installation des dépendances

```bash
# Créer un environnement virtuel
python -m venv venv

# Activer l'environnement virtuel
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate

# Installer les dépendances
pip install -r requirements.txt
```

### 2. Configuration de la base de données

```bash
# Démarrer PostgreSQL avec Docker
docker-compose up -d postgres

# Vérifier que PostgreSQL est démarré
docker-compose ps
```

### 3. Configuration de l'environnement

Créez un fichier `.env` à la racine du projet :

```env
# Database Configuration
DATABASE_URL=postgresql://fintel_user:fintel_password@localhost:5432/fintel_db
DB_HOST=localhost
DB_PORT=5432
DB_NAME=fintel_db
DB_USER=fintel_user
DB_PASSWORD=fintel_password

# JWT Configuration
SECRET_KEY=your-secret-key-here-change-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# OTP Configuration
OTP_EXPIRE_MINUTES=5
OTP_LENGTH=4

# API Configuration
API_V1_STR=/api/v1
PROJECT_NAME=Fintel API

# CORS Configuration
BACKEND_CORS_ORIGINS=["http://localhost:3000", "http://localhost:8080", "http://localhost:8000"]
```

### 4. Démarrage de l'API

```bash
# Démarrer l'API
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

L'API sera disponible sur : http://localhost:8000

## 📚 Documentation API

- **Swagger UI** : http://localhost:8000/docs
- **ReDoc** : http://localhost:8000/redoc

## 🔐 Endpoints d'Authentification

### Demander un code OTP
```http
POST /api/v1/auth/request-otp
Content-Type: application/json

{
  "phone_number": "0505979884"
}
```

### Vérifier le code OTP
```http
POST /api/v1/auth/verify-otp
Content-Type: application/json

{
  "phone_number": "0505979884",
  "otp_code": "1234"
}
```

### Connexion
```http
POST /api/v1/auth/login
Content-Type: application/json

{
  "phone_number": "0505979884",
  "password": "azerty"
}
```

## 💰 Endpoints de Transactions

### Récupérer le solde du portefeuille
```http
GET /api/v1/transactions/wallet
Authorization: Bearer <your_token>
```

### Créer un dépôt
```http
POST /api/v1/transactions/deposit
Authorization: Bearer <your_token>
Content-Type: application/json

{
  "transaction_type": "deposit",
  "amount": 10000.00,
  "currency": "XOF",
  "network": "orange",
  "description": "Dépôt via Orange Money"
}
```

### Créer un retrait
```http
POST /api/v1/transactions/withdrawal
Authorization: Bearer <your_token>
Content-Type: application/json

{
  "transaction_type": "withdrawal",
  "amount": 5000.00,
  "currency": "XOF",
  "network": "mtn",
  "description": "Retrait via MTN Money"
}
```

### Créer un transfert
```http
POST /api/v1/transactions/transfer
Authorization: Bearer <your_token>
Content-Type: application/json

{
  "transaction_type": "transfer",
  "amount": 2500.00,
  "currency": "XOF",
  "recipient_phone": "0701234567",
  "description": "Transfert vers un ami"
}
```

### Historique des transactions
```http
GET /api/v1/transactions/history?limit=20&offset=0
Authorization: Bearer <your_token>
```

## 🧪 Comptes de Test

### Utilisateur de test
- **Numéro** : `0505979884`
- **Code OTP** : `1234`
- **Mot de passe** : `azerty`

## 🐳 Gestion avec Docker

### Démarrer tous les services
```bash
docker-compose up -d
```

### Arrêter tous les services
```bash
docker-compose down
```

### Voir les logs
```bash
docker-compose logs -f
```

### Accéder à pgAdmin
- URL : http://localhost:5050
- Email : admin@fintel.com
- Mot de passe : admin123

## 🏗️ Structure du Projet

```
Fintel-backend/
├── app/
│   ├── api/
│   │   └── v1/
│   │       ├── auth.py          # Endpoints d'authentification
│   │       └── transactions.py  # Endpoints de transactions
│   ├── core/
│   │   ├── database.py          # Configuration de la base de données
│   │   └── security.py          # Fonctions de sécurité
│   ├── models/
│   │   ├── user.py              # Modèles User et OTP
│   │   └── transaction.py       # Modèles Transaction et Wallet
│   ├── schemas/
│   │   ├── user.py              # Schémas Pydantic pour les utilisateurs
│   │   └── transaction.py       # Schémas Pydantic pour les transactions
│   ├── services/
│   │   ├── user_service.py      # Logique métier pour les utilisateurs
│   │   └── transaction_service.py # Logique métier pour les transactions
│   └── main.py                  # Application FastAPI principale
├── config.py                    # Configuration de l'application
├── requirements.txt             # Dépendances Python
├── docker-compose.yml          # Configuration Docker
└── README.md                   # Documentation
```

## 🔧 Développement

### Tests
```bash
# Installer pytest
pip install pytest pytest-asyncio

# Exécuter les tests
pytest
```

### Formatage du code
```bash
# Installer black
pip install black

# Formater le code
black app/
```

## 📝 Notes

- L'API utilise JWT pour l'authentification
- Les mots de passe sont hachés avec bcrypt
- Les codes OTP expirent après 5 minutes
- Les tokens JWT expirent après 30 minutes
- CORS est configuré pour permettre les requêtes depuis le frontend mobile



