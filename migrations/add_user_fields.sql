-- Migration pour ajouter les nouveaux champs à la table users
-- Exécutez ce script sur votre base de données PostgreSQL

-- Ajouter les nouvelles colonnes
ALTER TABLE users 
ADD COLUMN IF NOT EXISTS whatsapp_number VARCHAR(20),
ADD COLUMN IF NOT EXISTS date_of_birth DATE,
ADD COLUMN IF NOT EXISTS country VARCHAR(100),
ADD COLUMN IF NOT EXISTS city VARCHAR(100),
ADD COLUMN IF NOT EXISTS address TEXT,
ADD COLUMN IF NOT EXISTS id_type VARCHAR(50),
ADD COLUMN IF NOT EXISTS id_number VARCHAR(100),
ADD COLUMN IF NOT EXISTS id_issue_date DATE,
ADD COLUMN IF NOT EXISTS id_expiry_date DATE,
ADD COLUMN IF NOT EXISTS profile_picture_url VARCHAR(500),
ADD COLUMN IF NOT EXISTS front_id_photo_url VARCHAR(500),
ADD COLUMN IF NOT EXISTS back_id_photo_url VARCHAR(500),
ADD COLUMN IF NOT EXISTS selfie_photo_url VARCHAR(500),
ADD COLUMN IF NOT EXISTS otp_delivery_preference VARCHAR(10) DEFAULT 'sms',
ADD COLUMN IF NOT EXISTS terms_accepted BOOLEAN DEFAULT FALSE,
ADD COLUMN IF NOT EXISTS privacy_policy_accepted BOOLEAN DEFAULT FALSE;

-- Vérifier que les colonnes ont été ajoutées
SELECT column_name, data_type, is_nullable, column_default
FROM information_schema.columns
WHERE table_name = 'users'
ORDER BY ordinal_position;

