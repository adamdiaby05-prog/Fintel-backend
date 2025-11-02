# 🗄️ Créer les Tables Manuellement (Solution Rapide)

## ❌ Problème

Le backend est déployé mais les tables ne sont pas créées dans la base de données.

## ✅ Solution IMMÉDIATE : Créer les tables manuellement

### Option 1 : Via un Client PostgreSQL (RECOMMANDÉ) ⭐

1. **Téléchargez TablePlus** (gratuit) : https://tableplus.com/
2. **Créez une nouvelle connexion PostgreSQL** :
   - **Name** : `Fintel Database`
   - **Host** : `213.199.48.58`
   - **Port** : `5432`
   - **User** : `postgres`
   - **Password** : `rs1sj5pdgx04mql5`
   - **Database** : `postgres`
3. **Connectez-vous**
4. **Ouvrez l'éditeur SQL** (Ctrl+N ou clic droit > "New Query")
5. **Copiez-collez** le script SQL ci-dessous
6. **Exécutez** le script (Ctrl+Enter)

### Script SQL à Exécuter

```sql
-- Table: users
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    phone_number VARCHAR(20) UNIQUE NOT NULL,
    whatsapp_number VARCHAR(20),
    email VARCHAR(255) UNIQUE,
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    date_of_birth DATE,
    country VARCHAR(100),
    city VARCHAR(100),
    address TEXT,
    id_type VARCHAR(50),
    id_number VARCHAR(100),
    id_issue_date DATE,
    id_expiry_date DATE,
    profile_picture_url TEXT,
    front_id_photo_url VARCHAR(500),
    back_id_photo_url VARCHAR(500),
    selfie_photo_url VARCHAR(500),
    otp_delivery_preference VARCHAR(10) DEFAULT 'sms',
    terms_accepted BOOLEAN DEFAULT FALSE,
    privacy_policy_accepted BOOLEAN DEFAULT FALSE,
    hashed_password VARCHAR(255),
    is_active BOOLEAN DEFAULT TRUE,
    is_verified BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE
);

-- Table: otps
CREATE TABLE IF NOT EXISTS otps (
    id SERIAL PRIMARY KEY,
    phone_number VARCHAR(20) NOT NULL,
    otp_code VARCHAR(10) NOT NULL,
    is_used BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    expires_at TIMESTAMP WITH TIME ZONE NOT NULL
);

-- Table: wallets
CREATE TABLE IF NOT EXISTS wallets (
    id SERIAL PRIMARY KEY,
    user_id INTEGER UNIQUE NOT NULL,
    balance NUMERIC(15, 2) DEFAULT 5000.00,
    currency VARCHAR(3) DEFAULT 'XOF',
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE,
    CONSTRAINT fk_wallet_user FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- Table: transactions
CREATE TABLE IF NOT EXISTS transactions (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL,
    transaction_type VARCHAR(50) NOT NULL,
    amount NUMERIC(15, 2) NOT NULL,
    currency VARCHAR(3) DEFAULT 'XOF',
    status VARCHAR(20) DEFAULT 'pending',
    description TEXT,
    reference VARCHAR(100) UNIQUE,
    network VARCHAR(50),
    recipient_phone VARCHAR(20),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE,
    CONSTRAINT fk_transaction_user FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- Index
CREATE INDEX IF NOT EXISTS idx_users_phone_number ON users(phone_number);
CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);
CREATE INDEX IF NOT EXISTS idx_otps_phone_number ON otps(phone_number);
CREATE INDEX IF NOT EXISTS idx_wallets_user_id ON wallets(user_id);
CREATE INDEX IF NOT EXISTS idx_transactions_user_id ON transactions(user_id);
CREATE INDEX IF NOT EXISTS idx_transactions_reference ON transactions(reference);
CREATE INDEX IF NOT EXISTS idx_transactions_created_at ON transactions(created_at DESC);

-- Fonction pour updated_at
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Triggers
DROP TRIGGER IF EXISTS update_users_updated_at ON users;
CREATE TRIGGER update_users_updated_at 
    BEFORE UPDATE ON users
    FOR EACH ROW 
    EXECUTE FUNCTION update_updated_at_column();

DROP TRIGGER IF EXISTS update_wallets_updated_at ON wallets;
CREATE TRIGGER update_wallets_updated_at 
    BEFORE UPDATE ON wallets
    FOR EACH ROW 
    EXECUTE FUNCTION update_updated_at_column();

DROP TRIGGER IF EXISTS update_transactions_updated_at ON transactions;
CREATE TRIGGER update_transactions_updated_at 
    BEFORE UPDATE ON transactions
    FOR EACH ROW 
    EXECUTE FUNCTION update_updated_at_column();

-- Vérification
SELECT 
    table_name,
    (SELECT COUNT(*) 
     FROM information_schema.columns 
     WHERE table_name = t.table_name 
     AND table_schema = 'public') as column_count
FROM information_schema.tables t
WHERE table_schema = 'public'
AND table_name IN ('users', 'otps', 'wallets', 'transactions')
ORDER BY table_name;
```

### Option 2 : Depuis GitHub (Plus Simple)

1. Allez sur : https://raw.githubusercontent.com/adamdiaby05-prog/Fintel-backend/main/migrations/init_database_complete.sql
2. **Copiez TOUT le contenu**
3. **Collez** dans votre client PostgreSQL
4. **Exécutez**

## ✅ Vérification

Après l'exécution, vérifiez avec :

```sql
SELECT table_name 
FROM information_schema.tables 
WHERE table_schema = 'public'
ORDER BY table_name;
```

Vous devriez voir **4 tables** :
- ✅ `otps`
- ✅ `transactions`
- ✅ `users`
- ✅ `wallets`

## 🔧 Correction du Backend pour l'Automatisation Future

Le code a été mis à jour pour créer automatiquement les tables au démarrage. 

**Pour appliquer la correction :**

1. Les modifications sont dans `app/main.py`
2. Poussez les changements sur GitHub
3. Redéployez le backend sur Dokploy
4. Les tables seront créées automatiquement au prochain démarrage

