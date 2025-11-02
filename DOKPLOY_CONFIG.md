# 🚀 Configuration Dokploy pour Fintel Backend

## 📋 Configuration du Déploiement

### 1. Source du Code ⚙️
Dans l'onglet **Deploy Settings** de Dokploy :

- **Provider** : `Github` ✅
- **Repository** : `adamdiaby05-prog/Fintel-backend`
- **Branch** : `main`
- **Build Path** : `/` (laisser vide ou mettre `/`)
- **Trigger Type** : `On Push` ✅
- **Watch Paths** : Laisser vide
- **Enable Submodules** : Désactivé
- **Build Type** : `Dockerfile` ⭐ (IMPORTANT!)

### 2. Variables d'Environnement

Dans l'onglet **Environment** de Dokploy, ajoutez ces variables :

```env
# Database Configuration (utiliser le nom interne du service)
DATABASE_URL=postgresql://postgres:rs1sj5pdgx04mql5@fintel-database-vlmpxo:5432/postgres

# JWT Configuration
SECRET_KEY=votre-cle-secrete-super-longue-changez-en-production-min-32-caracteres
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# API Configuration
API_V1_STR=/api/v1
PROJECT_NAME=Fintel API

# CORS Configuration (ajoutez l'URL de votre frontend)
BACKEND_CORS_ORIGINS=["*"]
```

⚠️ **IMPORTANT** : Remplacez `SECRET_KEY` par une clé secrète forte en production !

### 3. Port

- **Port interne** : `8000` (FastAPI écoute sur ce port)
- **Port externe** : Configurez selon vos besoins (ex: 8000)

### 4. Health Check (optionnel mais recommandé)

Ajoutez un endpoint de health check dans `app/main.py` :

```python
@app.get("/api/v1/health")
async def health_check():
    return {"status": "ok", "service": "Fintel API"}
```

## 🗄️ Initialisation de la Base de Données

**AVANT de démarrer l'application**, vous devez créer les tables dans votre base de données.

### Option 1 : Via l'interface Dokploy (RECOMMANDÉ) ⭐

1. Allez dans votre service de base de données `fintel-database-vlmpxo`
2. Cliquez sur l'onglet **"Database"** ou cherchez un **"SQL Editor"**
3. Ouvrez le fichier `migrations/init_database_complete.sql` depuis GitHub
4. Copiez **TOUT** le contenu
5. Collez et exécutez dans l'éditeur SQL
6. Vérifiez que les 4 tables sont créées :
   ```sql
   SELECT table_name 
   FROM information_schema.tables 
   WHERE table_schema = 'public';
   ```

### Option 2 : Via psql (si vous avez accès SSH)

```bash
# Depuis votre machine locale ou un conteneur
psql "postgresql://postgres:rs1sj5pdgx04mql5@213.199.48.58:5432/postgres" -f migrations/init_database_complete.sql
```

### Option 3 : Via un client PostgreSQL

Utilisez pgAdmin, DBeaver ou TablePlus :
- **Host** : `213.199.48.58` (ou `fintel-database-vlmpxo` en interne)
- **Port** : `5432`
- **Database** : `postgres`
- **User** : `postgres`
- **Password** : `rs1sj5pdgx04mql5`

## ✅ Vérification après Déploiement

### 1. Vérifier que les tables existent

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

### 2. Tester l'API

Une fois l'application déployée, testez :

```bash
# Health check
curl http://votre-domaine:8000/api/v1/health

# Documentation Swagger
# Ouvrez dans votre navigateur : http://votre-domaine:8000/docs
```

## 🔧 Configuration Avancée

### Commandes de Build (optionnel)

Si vous devez exécuter des commandes avant le build, ajoutez dans **Build Settings** :

```bash
# Aucune commande spéciale nécessaire avec Dockerfile
```

### Volumes (si nécessaire)

Pas de volume nécessaire pour le moment.

### Logs

Les logs seront disponibles dans l'onglet **Logs** de Dokploy.

## 📝 Checklist de Déploiement

- [ ] Code poussé sur GitHub ✅
- [ ] Base de données PostgreSQL déployée ✅
- [ ] Tables créées dans la base de données ⚠️ **À FAIRE**
- [ ] Variables d'environnement configurées
- [ ] Application déployée sur Dokploy
- [ ] Port 8000 configuré
- [ ] Health check fonctionne
- [ ] Documentation Swagger accessible

## 🆘 Résolution de Problèmes

### L'application ne démarre pas

1. Vérifiez les logs dans Dokploy
2. Vérifiez que `DATABASE_URL` est correct
3. Vérifiez que les tables existent dans la base de données

### Erreur de connexion à la base de données

- Utilisez le nom interne du service : `fintel-database-vlmpxo` (pas l'IP externe)
- Vérifiez que le service de base de données est démarré

### Tables non créées

- Exécutez le script SQL `migrations/init_database_complete.sql`
- Vérifiez les erreurs dans les logs de la base de données

