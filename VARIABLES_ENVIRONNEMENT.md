# 🔐 Variables d'Environnement pour Dokploy

## ✅ Configuration Correcte

Voici les variables d'environnement à configurer dans Dokploy pour votre backend :

### Variables d'Environnement (Dans l'onglet "Environment" de Dokploy)

```env
DATABASE_URL=postgresql://postgres:rs1sj5pdgx04mql5@fintel-database-vlmpxo:5432/postgres

SECRET_KEY=fintel-super-secret-key-change-this-in-production-2024-secure-token

ALGORITHM=HS256

ACCESS_TOKEN_EXPIRE_MINUTES=30

API_V1_STR=/api/v1

PROJECT_NAME=Fintel API

BACKEND_CORS_ORIGINS=["*"]
```

## ⚠️ Notes Importantes

### 1. SECRET_KEY
- ⚠️ **IMPORTANT** : Remplacez `SECRET_KEY` par une clé secrète unique et sécurisée !
- La clé doit faire **minimum 32 caractères**
- Utilisez une clé différente en production
- Ne partagez JAMAIS cette clé publiquement

**Générer une clé sécurisée** :
```python
import secrets
print(secrets.token_urlsafe(32))
```

### 2. DATABASE_URL
- ✅ Utilisez le **nom interne** `fintel-database-vlmpxo` (pas l'IP externe)
- ✅ Utilisez le **port interne** `5432`
- ⚠️ Si vous avez ajouté `DATABASE_URL` deux fois, **supprimez la duplication** et gardez une seule entrée

### 3. BACKEND_CORS_ORIGINS
- Pour le développement, `["*"]` autorise toutes les origines
- En production, remplacez par la liste des URLs autorisées :
  ```
  BACKEND_CORS_ORIGINS=["https://votre-domaine.com", "https://www.votre-domaine.com"]
  ```

## 📋 Checklist de Configuration

- [ ] `DATABASE_URL` configuré avec le nom interne du service
- [ ] `SECRET_KEY` remplacé par une clé sécurisée (minimum 32 caractères)
- [ ] `ALGORITHM` défini à `HS256`
- [ ] `ACCESS_TOKEN_EXPIRE_MINUTES` configuré (30 minutes)
- [ ] `API_V1_STR` défini à `/api/v1`
- [ ] `PROJECT_NAME` défini à `Fintel API`
- [ ] `BACKEND_CORS_ORIGINS` configuré
- [ ] Pas de duplication de variables

## 🚀 Après Configuration

Une fois les variables configurées :

1. **Déployez ou redéployez** votre backend
2. **Vérifiez les logs** pour s'assurer qu'il n'y a pas d'erreur
3. **Les tables seront créées automatiquement** au démarrage grâce à :
   ```python
   Base.metadata.create_all(bind=engine)
   ```
   dans `app/main.py`

## ✅ Vérification

Après le démarrage, vérifiez que les tables existent :

1. **Dans les logs du backend**, vous devriez voir :
   - `INFO:     Started server process`
   - Pas d'erreur de connexion à la base de données

2. **Testez l'API** :
   ```bash
   curl http://votre-domaine:8000/health
   ```

3. **Vérifiez la documentation Swagger** :
   ```
   http://votre-domaine:8000/docs
   ```

## 🔒 Générer une SECRET_KEY Sécurisée

Exécutez cette commande Python pour générer une clé sécurisée :

```python
import secrets
print(secrets.token_urlsafe(32))
```

Ou utilisez ce service en ligne : https://generate-secret.vercel.app/32

