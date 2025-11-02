-- Script pour vérifier et corriger les wallets individuels
-- IMPORTANT: Exécutez d'abord la section SELECT pour voir l'état actuel

-- 1. Afficher tous les wallets avec leurs utilisateurs
SELECT 
    w.id as wallet_id,
    w.user_id,
    u.phone_number,
    COALESCE(u.first_name || ' ', '') || COALESCE(u.last_name, 'Utilisateur') as user_name,
    w.balance,
    w.currency,
    w.created_at,
    w.updated_at
FROM wallets w
LEFT JOIN users u ON u.id = w.user_id
ORDER BY u.phone_number;

-- 2. Vérifier s'il y a des wallets dupliqués pour le même user_id (ne devrait jamais arriver)
SELECT 
    user_id,
    COUNT(*) as wallet_count,
    STRING_AGG(id::text, ', ') as wallet_ids,
    STRING_AGG(balance::text, ', ') as balances
FROM wallets
GROUP BY user_id
HAVING COUNT(*) > 1;

-- 3. Vérifier les utilisateurs sans wallet
SELECT 
    u.id,
    u.phone_number,
    COALESCE(u.first_name || ' ', '') || COALESCE(u.last_name, 'Utilisateur') as user_name
FROM users u
LEFT JOIN wallets w ON w.user_id = u.id
WHERE w.id IS NULL
ORDER BY u.phone_number;

-- 4. CORRECTION: Mettre des soldes individuels pour les tests
-- DÉCOMMENTEZ ET MODIFIEZ LES VALEURS SELON VOS BESOINS

-- Exemple: Mettre des soldes différents pour tester
-- UPDATE wallets SET balance = 3000.00, updated_at = NOW() 
-- WHERE user_id IN (SELECT id FROM users WHERE phone_number = '0506070809');

-- UPDATE wallets SET balance = 3000.00, updated_at = NOW() 
-- WHERE user_id IN (SELECT id FROM users WHERE phone_number = '0102030405');

-- 5. Créer des wallets pour les utilisateurs qui n'en ont pas (avec 5000 XOF par défaut)
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

