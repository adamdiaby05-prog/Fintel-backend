# 🗄️ EXÉCUTER LE SCRIPT SQL DANS LE TERMINAL DOKPLOY

## 📋 Instructions étape par étape

### Étape 1 : Accéder au terminal de la base de données

1. Dans Dokploy, allez à votre service **`fintel-database-vlmpxo`**
2. Cliquez sur l'onglet **"Terminal"** ou **"Shell"**
3. Vous serez connecté directement au conteneur PostgreSQL

### Étape 2 : Se connecter à PostgreSQL

Une fois dans le terminal, tapez :

```bash
psql -U postgres -d postgres
```

Vous serez invité à entrer le mot de passe : `rs1sj5pdgx04mql5`

### Étape 3 : Exécuter le script SQL

Vous avez **2 options** :

#### ✅ Option A : Copier-coller directement

1. Ouvrez le fichier `migrations/init_database_complete.sql` depuis GitHub :
   - https://github.com/adamdiaby05-prog/Fintel-backend/blob/main/migrations/init_database_complete.sql

2. **Copiez TOUT le contenu** du fichier

3. **Collez-le dans le terminal** où vous êtes connecté à `psql`

4. Le script s'exécutera automatiquement et affichera :
   - Les messages de création des tables
   - Les messages de création des index
   - Les messages de création des triggers
   - La vérification finale avec la liste des tables créées

#### ✅ Option B : Exécuter depuis un fichier (si le fichier est accessible)

Si vous avez accès au fichier sur le serveur, utilisez :

```bash
\i /chemin/vers/init_database_complete.sql
```

### Étape 4 : Vérifier les tables

Après l'exécution, vérifiez que les tables sont créées :

```sql
SELECT table_name 
FROM information_schema.tables 
WHERE table_schema = 'public'
ORDER BY table_name;
```

Vous devriez voir :
- ✅ `otps`
- ✅ `transactions`
- ✅ `users`
- ✅ `wallets`

### Étape 5 : Quitter psql

Une fois terminé, tapez :

```sql
\q
```

## 🎯 Commande complète (tout-en-un)

Si vous préférez, voici la commande complète en une seule ligne :

```bash
psql -U postgres -d postgres -c "$(curl -s https://raw.githubusercontent.com/adamdiaby05-prog/Fintel-backend/main/migrations/init_database_complete.sql)"
```

Ou si vous avez le fichier localement :

```bash
psql -U postgres -d postgres -f /chemin/vers/init_database_complete.sql
```

## 📝 Exemple de sortie attendue

Après l'exécution, vous devriez voir quelque chose comme :

```
CREATE TABLE
CREATE TABLE
CREATE TABLE
CREATE TABLE
CREATE INDEX
CREATE INDEX
...
✅ Toutes les tables ont été créées avec succès!
📊 Tables créées: users, otps, wallets, transactions

 table_name   | column_count 
--------------+--------------
 otps         |            6
 transactions |           11
 users        |           22
 wallets      |            7
(4 rows)
```

## 🆘 En cas d'erreur

### Erreur "relation already exists"
- Les tables existent déjà. C'est normal si vous avez déjà exécuté le script.
- Le script utilise `CREATE TABLE IF NOT EXISTS`, donc il est sûr de le réexécuter.

### Erreur de connexion
- Vérifiez que vous êtes dans le bon terminal (celui de la base de données)
- Vérifiez les identifiants : `postgres` / `rs1sj5pdgx04mql5`

### Erreur de permission
- Assurez-vous d'être connecté en tant que `postgres` (super-utilisateur)

