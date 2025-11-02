# 🔐 Informations de Connexion à la Base de Données Dokploy

## 📋 Champs à remplir dans l'interface de connexion

### Si vous voyez un formulaire avec ces champs, voici les valeurs :

**Server Name** (ou **Service**) : 
```
Fintel Database
```
(ou n'importe quel nom que vous voulez donner à cette connexion)

**Host name/address** (ou **Service**) :
```
213.199.48.58
```
(C'est l'adresse externe de votre base de données Dokploy)

**Port** :
```
5432
```

**Database** :
```
postgres
```

**User** (ou **Username**) :
```
postgres
```

**Password** :
```
rs1sj5pdgx04mql5
```

**Role** :
```
postgres
```
(ou laissez "Select an item..." si vous n'avez pas de rôle spécifique)

---

## 📝 Résumé complet

```
Server Name:     Fintel Database
Host/Address:    213.199.48.58
Port:            5432
Database:        postgres
User:            postgres
Password:        rs1sj5pdgx04mql5
Role:            postgres (ou laisser par défaut)
```

---

## ✅ Paramètres SSL (optionnel)

Si vous voyez un paramètre "SSL mode" :
- **SSL mode** : `prefer` ou `require`
- C'est généralement déjà configuré automatiquement

---

## 🎯 Après la connexion

Une fois connecté :
1. Vous aurez accès à un éditeur SQL
2. Ouvrez le fichier `migrations/init_database_complete.sql`
3. Copiez-collez tout le contenu
4. Exécutez le script
5. Vérifiez que les 4 tables sont créées !

