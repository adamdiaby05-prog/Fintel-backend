-- Migration pour ajouter 5000 FCFA à tous les portefeuilles existants
-- Ce script met à jour tous les wallets avec un solde de 5000 XOF pour les tests
-- Si un wallet existe déjà, son solde est mis à 5000 XOF (pas d'addition)
-- Si un wallet n'existe pas, il est créé avec 5000 XOF

-- Créer un wallet avec 5000 XOF pour chaque utilisateur qui n'en a pas
INSERT INTO wallets (user_id, balance, currency, is_active, created_at, updated_at)
SELECT 
    u.id,
    5000.00,
    'XOF',
    true,
    NOW(),
    NOW()
FROM users u
WHERE NOT EXISTS (
    SELECT 1 
    FROM wallets w 
    WHERE w.user_id = u.id
);

-- Mettre à jour tous les portefeuilles existants pour avoir 5000 XOF
UPDATE wallets
SET balance = 5000.00,
    updated_at = NOW();

-- Afficher le résultat pour vérification
SELECT 
    u.id,
    u.phone_number,
    COALESCE(u.first_name || ' ', '') || COALESCE(u.last_name, '') as name,
    w.balance,
    w.currency
FROM users u
LEFT JOIN wallets w ON w.user_id = u.id
ORDER BY u.id;
