# 🗄️ CRÉER LES TABLES DANS LA BASE DE DONNÉES

## ⚠️ IMPORTANT : Les tables doivent être créées AVANT de démarrer l'application !

## 🎯 Méthode RAPIDE (via l'interface Dokploy)

### Étape 1 : Accéder à l'éditeur SQL

1. Allez sur votre serveur Dokploy
2. Cliquez sur votre service de base de données : **`fintel-database-vlmpxo`**
3. Cherchez un onglet **"Database"**, **"SQL Editor"**, ou **"Query"**
4. Si vous ne trouvez pas, utilisez un client PostgreSQL (voir Option 2)

### Étape 2 : Exécuter le script SQL

1. **Ouvrez le fichier** `migrations/init_database_complete.sql` depuis GitHub :
   - Lien direct : https://github.com/adamdiaby05-prog/Fintel-backend/blob/main/migrations/init_database_complete.sql
   - Ou copiez depuis votre repo local

2. **Copiez TOUT le contenu** du fichier

3. **Collez** dans l'éditeur SQL de Dokploy

4. **Exécutez** le script (bouton "Run" ou "Execute")

### Étape 3 : Vérifier

Exécutez cette requête pour vérifier :

```sql
SELECT table_name 
FROM information_schema.tables 
WHERE table_schema = 'public'
ORDER BY table_name;
```

Vous devez voir **4 tables** :
- ✅ `otps`
- ✅ `transactions`
- ✅ `users`
- ✅ `wallets`

## 🔧 Option 2 : Via un client PostgreSQL

### Avec pgAdmin ou DBeaver

1. **Nouvelle connexion** :
   - **Host** : `213.199.48.58` (externe) ou `fintel-database-vlmpxo` (interne)
   - **Port** : `5432`
   - **Database** : `postgres`
   - **Username** : `postgres`
   - **Password** : `rs1sj5pdgx04mql5`

2. **Ouvrez** le fichier `migrations/init_database_complete.sql`

3. **Exécutez** le script

## 📝 Option 3 : Via psql (ligne de commande)

Si vous avez accès SSH ou psql installé :

```bash
psql "postgresql://postgres:rs1sj5pdgx04mql5@213.199.48.58:5432/postgres" -f migrations/init_database_complete.sql
```

## ✅ Après création des tables

Une fois les tables créées, vous pouvez :

1. **Démarrer votre application** sur Dokploy
2. **Vérifier les logs** pour s'assurer qu'il n'y a pas d'erreur
3. **Tester l'API** : `http://votre-domaine:8000/docs`

## 🆘 Si ça ne marche pas

1. **Vérifiez la connexion** à la base de données
2. **Vérifiez les logs** de la base de données pour les erreurs
3. **Assurez-vous** que vous êtes connecté à la bonne base (`postgres`)
4. **Vérifiez** que vous avez les permissions nécessaires

