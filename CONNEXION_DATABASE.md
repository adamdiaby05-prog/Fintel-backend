# 🔌 Guide de Connexion à la Base de Données Dokploy

## ❌ Erreur : "password authentication failed"

Cette erreur peut avoir plusieurs causes. Voici comment la résoudre :

## 🔍 Vérification des Credentials

### Option 1 : Utiliser les Credentials INTERNES (RECOMMANDÉ) ⭐

Depuis **votre application backend déployée sur Dokploy**, utilisez :

```
postgresql://postgres:rs1sj5pdgx04mql5@fintel-database-vlmpxo:5432/postgres
```

**IMPORTANT** : Utilisez le **nom du service** (`fintel-database-vlmpxo`) et non l'IP externe !

### Option 2 : Vérifier le mot de passe dans Dokploy

1. Allez dans votre service de base de données `fintel-database-vlmpxo`
2. Cliquez sur l'onglet **"General"** ou **"Internal Credentials"**
3. **Vérifiez** que le mot de passe est bien `rs1sj5pdgx04mql5`
4. Si le mot de passe est différent, **utilisez celui affiché** dans Dokploy

### Option 3 : Réinitialiser le mot de passe (si nécessaire)

Si vous avez oublié le mot de passe :

1. Dans Dokploy, allez dans votre service de base de données
2. Cherchez une option **"Reset Password"** ou **"Change Password"**
3. Ou supprimez et recréez le service (⚠️ perte de données si tables déjà créées)

## 🌐 Connexion depuis l'EXTÉRIEUR (votre machine locale)

Pour vous connecter depuis votre PC, vérifiez :

### 1. Port Externe activé

Dans Dokploy, pour votre base de données :
- **External Port** : Doit être configuré (ex: `5432`)
- **External Host** : `213.199.48.58` (l'IP de votre serveur)

### 2. Firewall

Vérifiez que le port `5432` n'est pas bloqué par un firewall.

### 3. Mot de passe correct

Utilisez le mot de passe affiché dans **"External Credentials"** si différent.

## ✅ Solution RECOMMANDÉE : Créer les tables depuis Dokploy

### Via l'interface Dokploy (le plus simple)

1. Allez dans votre service de base de données
2. Cherchez un onglet **"Database"**, **"SQL"**, ou **"Query"**
3. Si disponible, utilisez l'éditeur SQL intégré
4. Copiez le contenu de `migrations/init_database_complete.sql`
5. Exécutez-le directement dans l'interface

### Via un script Python dans l'application (alternative)

L'application peut créer les tables automatiquement au démarrage si vous configurez bien `DATABASE_URL` avec les credentials internes.

## 🔧 Configuration dans votre application backend

Dans les **variables d'environnement** de votre application backend sur Dokploy :

```env
DATABASE_URL=postgresql://postgres:rs1sj5pdgx04mql5@fintel-database-vlmpxo:5432/postgres
```

**Points importants** :
- ✅ Utilisez `fintel-database-vlmpxo` (nom interne) au lieu de l'IP
- ✅ Utilisez le port `5432` (port interne)
- ✅ Utilisez le mot de passe affiché dans **"Internal Credentials"**

## 📝 Checklist de Connexion

- [ ] Vérifié les credentials dans Dokploy
- [ ] Utilisé le nom de service interne (`fintel-database-vlmpxo`)
- [ ] Utilisé le port interne (`5432`)
- [ ] Utilisé le bon mot de passe (depuis Internal Credentials)
- [ ] Configuré `DATABASE_URL` dans les variables d'environnement de l'application
- [ ] Tables créées (via SQL ou automatiquement)

## 🆘 Si ça ne marche toujours pas

1. **Vérifiez les logs** de la base de données dans Dokploy
2. **Vérifiez** que le service de base de données est bien démarré
3. **Vérifiez** que les deux services (backend et database) sont sur le même réseau Dokploy
4. **Contactez** le support Dokploy si le problème persiste


