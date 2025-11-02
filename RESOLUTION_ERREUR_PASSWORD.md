# 🔐 Résolution : Erreur "password authentication failed"

## ❌ Problème

Vous voyez l'erreur :
```
connection failed: connection to server at "213.199.48.58", port 5432 failed: 
FATAL: password authentication failed for user "postgres"
```

## ✅ Solutions

### Solution 1 : Vérifier les credentials EXTERNES dans Dokploy (IMPORTANT) ⭐

Les credentials **externes** peuvent être **différents** des credentials **internes** !

1. **Allez dans votre service de base de données** `fintel-database-vlmpxo` dans Dokploy
2. **Ouvrez l'onglet "General"** ou cherchez **"External Credentials"**
3. **Vérifiez** les identifiants affichés pour la connexion **externe** :
   - **User** : peut être `postgres` ou différent
   - **Password** : peut être différent de `rs1sj5pdgx04mql5`
   - **Port externe** : peut être différent de `5432`
   - **Host externe** : `213.199.48.58`

4. **Utilisez ces credentials EXACTEMENT** tels qu'affichés dans Dokploy

### Solution 2 : Utiliser les credentials INTERNES (si connexion depuis Dokploy)

Si vous essayez de vous connecter depuis **l'intérieur de Dokploy** (via un conteneur backend), utilisez :

```
Host: fintel-database-vlmpxo  (nom du service, PAS l'IP)
Port: 5432
Database: postgres
User: postgres
Password: rs1sj5pdgx04mql5
```

### Solution 3 : Utiliser l'interface SQL de Dokploy (LE PLUS SIMPLE) ⭐⭐⭐

**Au lieu de vous connecter depuis l'extérieur**, utilisez l'interface intégrée de Dokploy :

1. **Allez dans votre service** `fintel-database-vlmpxo`
2. **Cherchez un onglet** :
   - "Database"
   - "SQL Editor"
   - "Query"
   - "Execute SQL"
   - "Database Tools"
   - "pgAdmin" (si disponible)
3. **Si vous trouvez un éditeur SQL**, utilisez-le directement
4. **Copiez-collez** le script `migrations/init_database_complete.sql`
5. **Exécutez** le script

Cette méthode ne nécessite **aucune connexion externe** !

### Solution 4 : Vérifier le Port Externe

1. Dans Dokploy, vérifiez que le **"External Port"** est bien configuré
2. Il peut être différent de `5432` (ex: `5433`, `54321`, etc.)
3. Utilisez le port affiché dans **"External Port"**

### Solution 5 : Réinitialiser le mot de passe externe

Si vous ne trouvez pas les credentials :

1. Dans Dokploy, cherchez une option **"Reset External Password"** ou **"Change Password"**
2. Ou **supprimez et recréez** le service (⚠️ perte de données si tables déjà créées)

## 🎯 Ce que vous devriez vérifier dans Dokploy

Dans l'onglet de votre base de données, vous devriez voir deux sections :

### Internal Credentials (pour connexions internes)
```
User: postgres
Password: rs1sj5pdgx04mql5
Host: fintel-database-vlmpxo
Port: 5432
```

### External Credentials (pour connexions depuis votre PC)
```
User: ??? (vérifiez dans Dokploy)
Password: ??? (vérifiez dans Dokploy - peut être différent !)
Host: 213.199.48.58
Port: ??? (vérifiez - peut être différent de 5432)
```

## ✅ Solution RECOMMANDÉE

**Utilisez l'interface SQL de Dokploy** si disponible - c'est la méthode la plus simple et elle ne nécessite pas de credentials externes !

Sinon, **vérifiez les "External Credentials"** dans Dokploy et utilisez exactement les valeurs affichées.

