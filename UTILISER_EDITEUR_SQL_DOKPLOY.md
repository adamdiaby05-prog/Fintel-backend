# 🎯 Utiliser l'Éditeur SQL Intégré de Dokploy

## ✅ Votre Configuration (Correcte)

D'après ce que vous avez partagé :
- **Internal Credentials** : `postgres` / `rs1sj5pdgx04mql5` ✅
- **External Credentials** : `postgres` / `rs1sj5pdgx04mql5` ✅

## 🔍 Trouver l'Éditeur SQL dans Dokploy

Dans votre interface Dokploy pour `fintel-database-vlmpxo`, cherchez :

### Onglets à vérifier :
1. **"Database"** - peut contenir un éditeur SQL
2. **"SQL"** ou **"SQL Editor"**
3. **"Query"** ou **"Query Tool"**
4. **"Execute"** ou **"Execute SQL"**
5. **"Tools"** - peut contenir des outils de base de données
6. **"pgAdmin"** - interface graphique PostgreSQL complète

### Si vous trouvez un éditeur SQL :

1. **Ouvrez l'éditeur SQL**
2. **Copiez TOUT le contenu** de ce fichier :
   - GitHub : https://raw.githubusercontent.com/adamdiaby05-prog/Fintel-backend/main/migrations/init_database_complete.sql
   - Ou ouvrez `Fintel-backend/migrations/init_database_complete.sql` localement
3. **Collez** dans l'éditeur SQL
4. **Exécutez** le script (bouton "Run", "Execute", ou F5)
5. **Vérifiez** que vous voyez "CREATE TABLE" pour chaque table

## 🔧 Si l'éditeur SQL n'existe pas dans Dokploy

### Option 1 : Utiliser pgAdmin via Docker (si disponible)

Certaines installations de Dokploy ont pgAdmin intégré. Cherchez un lien ou un bouton "pgAdmin" ou "Web Interface".

### Option 2 : Activer la connexion externe

Si le port externe n'est pas accessible :

1. **Vérifiez que "External Port (Internet)" est bien `5432`** ✅ (c'est bon d'après vos infos)
2. **Vérifiez le firewall** - le port 5432 doit être ouvert
3. **Testez la connexion** depuis votre PC avec :

```bash
# Dans PowerShell ou CMD
telnet 213.199.48.58 5432
```

Si ça ne fonctionne pas, le port est peut-être bloqué.

### Option 3 : Utiliser les credentials INTERNES depuis le backend

Au lieu de vous connecter depuis l'extérieur, **laissez le backend créer les tables automatiquement** :

1. **Déployez votre backend** avec cette variable d'environnement :
   ```
   DATABASE_URL=postgresql://postgres:rs1sj5pdgx04mql5@fintel-database-vlmpxo:5432/postgres
   ```

2. **Le backend créera automatiquement les tables** au démarrage grâce à cette ligne dans `app/main.py` :
   ```python
   Base.metadata.create_all(bind=engine)
   ```

## 📝 Checklist

- [ ] Cherché un onglet "Database", "SQL", "Query" dans Dokploy
- [ ] Trouvé un éditeur SQL intégré
- [ ] Copié le script `init_database_complete.sql`
- [ ] Exécuté le script
- [ ] Vérifié que les 4 tables sont créées

## 🎯 Solution la PLUS SIMPLE

**Déployez d'abord votre backend**, et il créera les tables automatiquement au démarrage ! 

Vous n'avez pas besoin de créer les tables manuellement si vous configurez bien `DATABASE_URL` avec les credentials internes.

