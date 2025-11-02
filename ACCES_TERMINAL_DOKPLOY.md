# 🔧 Accéder au Terminal de la Base de Données dans Dokploy

## ❌ Si vous voyez l'erreur "No such container: select-a-container"

Cela signifie que vous n'avez pas sélectionné le bon service ou que le terminal n'est pas accessible directement.

## ✅ Solutions

### Solution 1 : Via l'interface Web SQL de Dokploy (LE PLUS SIMPLE) ⭐

1. **Allez dans votre service de base de données** `fintel-database-vlmpxo`
2. **Cherchez un onglet "Database", "SQL Editor", "Query", ou "Execute"**
3. Si vous trouvez un éditeur SQL, **copiez-collez le script directement dedans**
4. **Exécutez** le script

### Solution 2 : Via un Client PostgreSQL Externe (RECOMMANDÉ)

Utilisez un client PostgreSQL comme **pgAdmin**, **DBeaver**, **TablePlus**, ou même **psql** depuis votre machine locale.

#### Avec psql (ligne de commande)

Sur votre machine Windows, si vous avez PostgreSQL installé :

```bash
# Installer PostgreSQL client si nécessaire
# Télécharger depuis : https://www.postgresql.org/download/windows/

# Puis connectez-vous :
psql -h 213.199.48.58 -p 5432 -U postgres -d postgres
```

Mot de passe : `rs1sj5pdgx04mql5`

#### Avec TablePlus (Interface graphique - GRATUIT) ⭐ RECOMMANDÉ

1. **Téléchargez TablePlus** : https://tableplus.com/
2. **Créez une nouvelle connexion PostgreSQL** :
   - **Name** : `Fintel Database`
   - **Host** : `213.199.48.58`
   - **Port** : `5432`
   - **User** : `postgres`
   - **Password** : `rs1sj5pdgx04mql5`
   - **Database** : `postgres`
3. **Connectez-vous**
4. **Ouvrez l'éditeur SQL** (clic droit sur la connexion > "New Query" ou Ctrl+N)
5. **Copiez-collez** le contenu de `migrations/init_database_complete.sql`
6. **Exécutez** le script (Ctrl+Enter ou bouton "Run")

#### Avec DBeaver (GRATUIT et Open Source)

1. **Téléchargez DBeaver** : https://dbeaver.io/download/
2. **Créez une nouvelle connexion PostgreSQL** :
   - **Host** : `213.199.48.58`
   - **Port** : `5432`
   - **Database** : `postgres`
   - **Username** : `postgres`
   - **Password** : `rs1sj5pdgx04mql5`
3. **Connectez-vous**
4. **Ouvrez l'éditeur SQL**
5. **Copiez-collez** et **exécutez** le script

### Solution 3 : Via un Conteneur Backend Temporaire

Si vous avez déjà déployé votre backend, vous pouvez créer un conteneur temporaire pour exécuter psql :

1. **Dans Dokploy**, créez un nouveau service temporaire ou utilisez un conteneur existant
2. **Utilisez une image PostgreSQL client** :
   ```bash
   docker run -it --rm postgres:15 psql "postgresql://postgres:rs1sj5pdgx04mql5@213.199.48.58:5432/postgres"
   ```

### Solution 4 : Exécuter le Script SQL Directement via URL

Si Dokploy a une fonctionnalité "Execute SQL from URL" :

```
https://raw.githubusercontent.com/adamdiaby05-prog/Fintel-backend/main/migrations/init_database_complete.sql
```

## 🎯 Méthode la PLUS SIMPLE (Recommandée)

**Utilisez TablePlus ou DBeaver** - c'est la méthode la plus facile et la plus visuelle !

1. Téléchargez TablePlus (gratuit et simple)
2. Configurez la connexion avec les identifiants Dokploy
3. Copiez-collez le script SQL
4. Exécutez

## 📝 Identifiants de Connexion

```
Host: 213.199.48.58 (ou fintel-database-vlmpxo en interne)
Port: 5432
Database: postgres
Username: postgres
Password: rs1sj5pdgx04mql5
```

## ✅ Vérification après Exécution

Une fois le script exécuté, vérifiez avec cette requête :

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

