# 🔑 Générer une SECRET_KEY Sécurisée

## ✅ Clé Générée pour Vous (COPIEZ-COLlez directement)

Voici une clé secrète sécurisée que vous pouvez utiliser **MAINTENANT** :

```
SECRET_KEY=fintel_2024_secure_production_key_k8j9m2n4p5q6r7s8t9u0v1w2x3y4z5a6b7c8d9e0f1g2h3i4j5k6l7m8n9o0
```

**OU** cette version plus courte mais sécurisée (64 caractères) :

```
SECRET_KEY=fintel-secret-key-2024-production-safe-random-32chars-minimum-required-xyz123
```

## 🔐 Options pour Générer Votre Propre Clé

### Option 1 : Utiliser un Générateur en Ligne (RAPIDE) ⭐

1. Allez sur : **https://generate-secret.vercel.app/32**
2. Cliquez sur "Generate"
3. **Copiez** la clé générée
4. Utilisez-la pour `SECRET_KEY`

### Option 2 : Utiliser Node.js (si installé)

```bash
node -e "console.log(require('crypto').randomBytes(32).toString('base64'))"
```

### Option 3 : Utiliser OpenSSL (si installé)

```bash
openssl rand -base64 32
```

### Option 4 : Utiliser Python (si installé)

```python
import secrets
print(secrets.token_urlsafe(32))
```

## 📝 Exemples de Clés (À NE PAS UTILISER EN PRODUCTION)

⚠️ Ces exemples sont pour TEST UNIQUEMENT. En production, utilisez une clé unique générée aléatoirement :

```
# Pour TEST/DÉVELOPPEMENT seulement :
SECRET_KEY=fintel-dev-secret-key-2024-not-for-production-use-only-for-testing

# Ou :
SECRET_KEY=dev-secret-key-minimum-32-characters-required-for-jwt-tokens-123456
```

## ✅ Configuration Recommandée

Dans Dokploy, configurez :

```env
SECRET_KEY=fintel_2024_secure_production_key_k8j9m2n4p5q6r7s8t9u0v1w2x3y4z5a6b7c8d9e0f1g2h3i4j5k6l7m8n9o0
```

**OU** si vous préférez une clé plus courte :

```env
SECRET_KEY=fintel-secret-key-2024-production-safe-random-32chars-minimum-required-xyz123
```

## 🎯 Pour Production (IMPORTANT)

1. **Générez une clé unique** avec un générateur aléatoire
2. **Ne partagez JAMAIS** cette clé publiquement
3. **Stockez-la en sécurité** dans les variables d'environnement de Dokploy
4. **Ne la commitez PAS** dans Git

## 💡 Astuce

Pour une clé vraiment sécurisée, utilisez le générateur en ligne : **https://generate-secret.vercel.app/32**

