# 🗄️ Initialisation de la Base de Données

Votre base de données PostgreSQL est déployée sur Dokploy mais ne contient pas encore de tables.

## Méthode 1 : Utiliser le Script SQL (RECOMMANDÉ) ⭐

### Option A : Via l'interface Dokploy

1. Allez dans votre service de base de données sur Dokploy
2. Cliquez sur **"Database"** ou **"SQL Editor"**
3. Copiez le contenu complet du fichier `migrations/init_database_complete.sql`
4. Collez-le dans l'éditeur SQL
5. Exécutez le script

### Option B : Via psql (ligne de commande)

```bash
# Si vous avez psql installé localement
psql "postgresql://postgres:rs1sj5pdgx04mql5@213.199.48.58:5432/postgres" -f migrations/init_database_complete.sql
```

### Option C : Via un client PostgreSQL (pgAdmin, DBeaver, etc.)

1. Connectez-vous à votre base de données avec :
   - **Host**: `213.199.48.58`
   - **Port**: `5432`
   - **Database**: `postgres`
   - **User**: `postgres`
   - **Password**: `rs1sj5pdgx04mql5`

2. Ouvrez le fichier `migrations/init_database_complete.sql`
3. Exécutez-le

## Méthode 2 : Utiliser le Script Python

### Prérequis

1. Installez les dépendances :
   ```bash
   pip install -r requirements.txt
   ```

2. Configurez la variable d'environnement `DATABASE_URL` :
   ```bash
   # Windows PowerShell
   $env:DATABASE_URL="postgresql://postgres:rs1sj5pdgx04mql5@fintel-database-vlmpxo:5432/postgres"
   
   # Linux/Mac
   export DATABASE_URL="postgresql://postgres:rs1sj5pdgx04mql5@fintel-database-vlmpxo:5432/postgres"
   ```

   **OU** créez un fichier `.env` :
   ```env
   DATABASE_URL=postgresql://postgres:rs1sj5pdgx04mql5@fintel-database-vlmpxo:5432/postgres
   ```

3. Exécutez le script :
   ```bash
   python init_database.py
   ```

## ✅ Vérification

Après l'initialisation, vérifiez que les tables existent :

```sql
SELECT table_name 
FROM information_schema.tables 
WHERE table_schema = 'public'
ORDER BY table_name;
```

Vous devriez voir :
- `otps`
- `transactions`
- `users`
- `wallets`

## 📋 Checklist

- [ ] Script SQL exécuté ou script Python exécuté
- [ ] 4 tables créées (users, otps, wallets, transactions)
- [ ] Index créés
- [ ] Triggers créés pour `updated_at`
- [ ] Vérification des tables effectuée

## 🔗 URLs de connexion

**Interne (depuis l'application déployée sur Dokploy)** :
```
postgresql://postgres:rs1sj5pdgx04mql5@fintel-database-vlmpxo:5432/postgres
```

**Externe (depuis votre machine locale)** :
```
postgresql://postgres:rs1sj5pdgx04mql5@213.199.48.58:5432/postgres
```

