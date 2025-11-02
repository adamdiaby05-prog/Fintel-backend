# Instructions pour corriger le type de colonne profile_picture_url

## Problème
Le champ `profile_picture_url` est défini comme `VARCHAR(500)` ce qui est trop petit pour stocker des images base64 (qui peuvent facilement dépasser 50 000 caractères).

## Solution
Changer le type de `VARCHAR(500)` à `TEXT` pour supporter des chaînes de caractères plus longues.

## Commande à exécuter

```bash
psql -U postgres -d fintel -f "C:\Users\ROG\Documents\fintel\Fintel-backend\migrations\fix_profile_picture_url_type.sql"
```

Ou si vous êtes déjà dans le répertoire :

```bash
psql -U postgres -d fintel -f migrations/fix_profile_picture_url_type.sql
```

## Vérification
Après la migration, vérifiez avec :

```sql
\d users
```

La colonne `profile_picture_url` devrait maintenant être de type `text` au lieu de `character varying(500)`.

