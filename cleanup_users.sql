-- Script SQL pour nettoyer les utilisateurs sans numéro de téléphone
DELETE FROM users WHERE phone_number IS NULL OR phone_number = '';

-- Vérifier les utilisateurs restants
SELECT id, phone_number, email, hashed_password IS NOT NULL as has_password 
FROM users;

