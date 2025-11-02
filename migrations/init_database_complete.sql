-- =====================================================
-- Script d'initialisation COMPLET de la base de données Fintel
-- À exécuter sur votre base de données PostgreSQL déployée sur Dokploy
-- =====================================================

-- =====================================================
-- 1. CRÉATION DES TABLES
-- =====================================================

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

-- =====================================================
-- 2. CRÉATION DES INDEX
-- =====================================================

-- Index pour users
CREATE INDEX IF NOT EXISTS idx_users_phone_number ON users(phone_number);
CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);

-- Index pour otps
CREATE INDEX IF NOT EXISTS idx_otps_phone_number ON otps(phone_number);
CREATE INDEX IF NOT EXISTS idx_otps_created_at ON otps(created_at DESC);

-- Index pour wallets
CREATE INDEX IF NOT EXISTS idx_wallets_user_id ON wallets(user_id);

-- Index pour transactions
CREATE INDEX IF NOT EXISTS idx_transactions_user_id ON transactions(user_id);
CREATE INDEX IF NOT EXISTS idx_transactions_reference ON transactions(reference);
CREATE INDEX IF NOT EXISTS idx_transactions_created_at ON transactions(created_at DESC);
CREATE INDEX IF NOT EXISTS idx_transactions_status ON transactions(status);

-- =====================================================
-- 3. FONCTION POUR MISE À JOUR AUTOMATIQUE DE updated_at
-- =====================================================

CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

-- =====================================================
-- 4. CRÉATION DES TRIGGERS
-- =====================================================

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

-- =====================================================
-- 5. VÉRIFICATION
-- =====================================================

DO $$
DECLARE
    table_count INTEGER;
BEGIN
    SELECT COUNT(*) INTO table_count
    FROM information_schema.tables
    WHERE table_schema = 'public'
    AND table_name IN ('users', 'otps', 'wallets', 'transactions');
    
    IF table_count = 4 THEN
        RAISE NOTICE '✅ Toutes les tables ont été créées avec succès!';
        RAISE NOTICE '📊 Tables créées: users, otps, wallets, transactions';
    ELSE
        RAISE WARNING '⚠️ Nombre de tables incorrect: % (attendu: 4)', table_count;
    END IF;
END $$;

-- Afficher les tables créées
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

