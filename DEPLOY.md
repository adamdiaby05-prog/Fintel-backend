# Guide de déploiement sur Dokploy

## 🗄️ Initialisation de la base de données

Votre base de données PostgreSQL est déployée sur Dokploy mais ne contient pas encore de tables. 

### Méthode 1 : Utiliser le script SQL (RECOMMANDÉ)

1. **Connectez-vous à votre base de données PostgreSQL** via Dokploy ou un client PostgreSQL (pgAdmin, DBeaver, etc.)

2. **Exécutez le script SQL** `migrations/init_database.sql` :
   ```sql
   -- Copiez le contenu de migrations/init_database.sql
   -- et exécutez-le dans votre client PostgreSQL
   ```

3. **Ou utilisez psql** depuis votre terminal :
   ```bash
   psql "postgresql://postgres:rs1sj5pdgx04mql5@213.199.48.58:5432/postgres" -f migrations/init_database.sql
   ```

### Méthode 2 : Utiliser le script Python

1. **Configurez votre `.env`** avec les credentials de votre base de données :
   ```env
   DATABASE_URL=postgresql://postgres:rs1sj5pdgx04mql5@fintel-database-vlmpxo:5432/postgres
   ```

2. **Exécutez le script d'initialisation** :
   ```bash
   python init_database.py
   ```

## 🚀 Configuration pour Dokploy

### Variables d'environnement nécessaires

Dans les paramètres de déploiement de votre application sur Dokploy, configurez :

```env
# Database (utiliser le nom interne du service)
DATABASE_URL=postgresql://postgres:rs1sj5pdgx04mql5@fintel-database-vlmpxo:5432/postgres

# JWT Configuration
SECRET_KEY=your-super-secret-key-change-this-in-production-min-32-chars
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# API Configuration
API_V1_STR=/api/v1
PROJECT_NAME=Fintel API

# CORS Configuration (ajoutez l'URL de votre frontend mobile)
BACKEND_CORS_ORIGINS=["*"]  # Pour le développement, restreindre en production
```

### Port d'exposition

L'API FastAPI écoute sur le port **8000** par défaut.

### Health Check

L'endpoint de health check est disponible sur :
```
GET /api/v1/health
```

## 📋 Checklist de déploiement

- [ ] Base de données PostgreSQL déployée ✅
- [ ] Tables créées dans la base de données
- [ ] Variables d'environnement configurées
- [ ] Application déployée sur Dokploy
- [ ] Tests de connexion à la base de données
- [ ] Tests des endpoints API

## 🔍 Vérification après déploiement

### Vérifier que les tables existent

Connectez-vous à votre base de données et exécutez :

```sql
SELECT table_name 
FROM information_schema.tables 
WHERE table_schema = 'public';
```

Vous devriez voir :
- `users`
- `otps`
- `wallets`
- `transactions`

### Tester l'API

```bash
# Health check
curl http://votre-serveur:8000/api/v1/health

# Documentation Swagger
http://votre-serveur:8000/docs
```

## 📝 Notes importantes

- ⚠️ **Ne commitez JAMAIS** le fichier `.env` avec les mots de passe réels
- 🔒 Changez le `SECRET_KEY` en production
- 🌐 Configurez `BACKEND_CORS_ORIGINS` avec les URLs réelles de votre frontend
- 💾 Faites des backups réguliers de votre base de données

