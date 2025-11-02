# Instructions pour corriger la base de données

## Problème
Il y a un utilisateur dans la base de données sans numéro de téléphone, ce qui cause des erreurs lors de l'inscription et de la connexion.

## Solution

Exécutez cette commande SQL directement dans PostgreSQL :

```sql
DELETE FROM users WHERE phone_number IS NULL OR phone_number = '';
```

Puis vérifiez que la table est vide ou contient seulement des utilisateurs valides :

```sql
SELECT id, phone_number, email, hashed_password IS NOT NULL as has_password 
FROM users;
```

## Commandes à exécuter dans psql

1. Ouvrez psql :
```bash
psql -U postgres -d fintel
```

2. Entrez le mot de passe : `0000`

3. Exécutez :
```sql
DELETE FROM users WHERE phone_number IS NULL OR phone_number = '';
SELECT * FROM users;
```

4. Si tout est correct, la table `users` devrait être vide (ou ne contenir que des utilisateurs avec un `phone_number` valide).

