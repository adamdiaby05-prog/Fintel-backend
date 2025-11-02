-- Migration pour corriger les soldes individuels des wallets
-- Ce script vérifie et affiche les wallets existants sans les modifier
-- Pour réinitialiser les soldes, exécutez manuellement les UPDATE ci-dessous

-- Afficher tous les wallets actuels
SELECT 
    w.id as wallet_id,
    w.user_id,
    u.phone_number,
    COALESCE(u.first_name || ' ', '') || COALESCE(u.last_name, '') as user_name,
    w.balance,
    w.currency,
    w.created_at,
    w.updated_at
FROM wallets w
LEFT JOIN users u ON u.id = w.user_id
ORDER BY w.user_id;

-- Vérifier s'il y a des wallets dupliqués pour le même user_id
SELECT 
    user_id,
    COUNT(*) as wallet_count,
    STRING_AGG(id::text, ', ') as wallet_ids
FROM wallets
GROUP BY user_id
HAVING COUNT(*) > 1;

-- Si vous voulez réinitialiser les soldes (DÉCOMMENTEZ LES LIGNES CI-DESSOUS):
-- ATTENTION: Cela écrasera tous les soldes existants!

-- UPDATE wallets SET balance = 3000.00 WHERE user_id IN (
--     SELECT id FROM users WHERE phone_number IN ('0506070809', '0102030405')
-- );

