# Rechargement des comptes pour les tests

## Script de migration SQL

Le fichier `add_5000_to_all_wallets.sql` permet de :
- Créer un wallet avec 5000 XOF pour chaque utilisateur qui n'en a pas
- Mettre à jour tous les wallets existants pour avoir 5000 XOF

## Exécution de la migration

### Méthode 1 : Via psql (ligne de commande)

```bash
psql -U postgres -d fintel -f "C:\Users\ROG\Documents\fintel\Fintel-backend\migrations\add_5000_to_all_wallets.sql"
```

### Méthode 2 : Copier-coller dans psql

1. Ouvrir psql :
```bash
psql -U postgres -d fintel
```

2. Copier le contenu de `add_5000_to_all_wallets.sql` et coller dans la console psql

## Vérification

Après l'exécution, tous les utilisateurs devraient avoir un wallet avec un solde de 5000 XOF.

Pour vérifier :
```sql
SELECT 
    u.id,
    u.phone_number,
    COALESCE(u.first_name || ' ', '') || COALESCE(u.last_name, '') as name,
    w.balance,
    w.currency
FROM users u
LEFT JOIN wallets w ON w.user_id = u.id
ORDER BY u.id;
```

## Note importante

Les nouveaux wallets créés automatiquement par l'application auront aussi un solde initial de 5000 XOF grâce à la modification dans `transaction_service.py`.

