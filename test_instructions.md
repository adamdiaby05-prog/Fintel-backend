# Instructions pour tester la sauvegarde des données

## Prérequis

1. **Démarrer le backend FastAPI** :
   ```bash
   cd Fintel-backend
   python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

2. **Vérifier que PostgreSQL est démarré** et que la base de données existe :
   ```bash
   psql -U postgres -d fintel
   ```

3. **Exécuter la migration** (si pas déjà fait) :
   ```bash
   psql -U postgres -d fintel -f migrations/add_user_fields.sql
   ```

## Option 1 : Test Automatique (Recommandé)

### Installer les dépendances pour les tests
```bash
pip install requests
```

### Exécuter le script de test
```bash
cd Fintel-backend
python test_user_profile.py
```

Le script va :
1. Vérifier que l'API est accessible
2. Tester l'inscription d'un utilisateur
3. Tester la sauvegarde des informations de contact
4. Tester la sauvegarde des informations personnelles
5. Tester la sauvegarde des informations d'identité
6. Tester la sauvegarde des informations de sécurité
7. Vérifier que toutes les données sont bien récupérées

## Option 2 : Test Manuel avec l'application Flutter

1. **Démarrer le backend** (déjà fait)
2. **Démarrer l'application Flutter**
3. **Suivre le processus d'inscription** :
   - Page de contact : Remplir téléphone, WhatsApp, email
   - Page d'informations personnelles : Remplir nom, prénom, date de naissance, pays, ville
   - Page d'identification : Remplir type de pièce, numéro, dates
   - Page de sécurité : Remplir mot de passe, accepter les termes

4. **Vérifier dans la base de données** :
   ```sql
   SELECT * FROM users WHERE phone_number = '0505979884';
   ```

## Option 3 : Test avec cURL ou Postman

### 1. Inscrire un utilisateur
```bash
curl -X POST http://192.168.100.7:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{"phone_number": "0505979884", "password": "test123"}'
```

### 2. Mettre à jour les informations de contact
```bash
curl -X PUT http://192.168.100.7:8000/api/v1/user/profile \
  -H "Content-Type: application/json" \
  -d '{
    "phone_number": "0505979884",
    "whatsapp_number": "0505979884",
    "email": "adamdiaby05@gmail.com",
    "otp_delivery_preference": "sms"
  }'
```

### 3. Mettre à jour les informations personnelles
```bash
curl -X PUT http://192.168.100.7:8000/api/v1/user/profile \
  -H "Content-Type: application/json" \
  -d '{
    "phone_number": "0505979884",
    "first_name": "Adam",
    "last_name": "diaby",
    "date_of_birth": "2000-01-15",
    "country": "Cote d'\''Ivoire",
    "city": "Sassandra"
  }'
```

### 4. Mettre à jour les informations d'identité
```bash
curl -X PUT http://192.168.100.7:8000/api/v1/user/profile \
  -H "Content-Type: application/json" \
  -d '{
    "phone_number": "0505979884",
    "id_type": "Carte d'\''Identité",
    "id_number": "ci hhhhb",
    "id_issue_date": "2000-01-22",
    "id_expiry_date": "2000-01-28"
  }'
```

### 5. Mettre à jour les informations de sécurité
```bash
curl -X PUT http://192.168.100.7:8000/api/v1/user/profile \
  -H "Content-Type: application/json" \
  -d '{
    "phone_number": "0505979884",
    "password": "azerty",
    "terms_accepted": true,
    "privacy_policy_accepted": true
  }'
```

### 6. Récupérer le profil complet
```bash
curl http://192.168.100.7:8000/api/v1/user/profile?phone=0505979884
```

## Vérification directe dans PostgreSQL

```sql
-- Voir tous les champs d'un utilisateur
SELECT 
    id,
    phone_number,
    whatsapp_number,
    email,
    first_name,
    last_name,
    date_of_birth,
    country,
    city,
    id_type,
    id_number,
    id_issue_date,
    id_expiry_date,
    otp_delivery_preference,
    terms_accepted,
    privacy_policy_accepted,
    is_active,
    is_verified,
    created_at,
    updated_at
FROM users 
WHERE phone_number = '0505979884';
```

## Vérifier que tous les champs sont remplis

```sql
SELECT 
    phone_number,
    CASE WHEN whatsapp_number IS NOT NULL THEN '✅' ELSE '❌' END as whatsapp,
    CASE WHEN email IS NOT NULL THEN '✅' ELSE '❌' END as email,
    CASE WHEN first_name IS NOT NULL THEN '✅' ELSE '❌' END as first_name,
    CASE WHEN last_name IS NOT NULL THEN '✅' ELSE '❌' END as last_name,
    CASE WHEN date_of_birth IS NOT NULL THEN '✅' ELSE '❌' END as date_of_birth,
    CASE WHEN country IS NOT NULL THEN '✅' ELSE '❌' END as country,
    CASE WHEN city IS NOT NULL THEN '✅' ELSE '❌' END as city,
    CASE WHEN id_type IS NOT NULL THEN '✅' ELSE '❌' END as id_type,
    CASE WHEN id_number IS NOT NULL THEN '✅' ELSE '❌' END as id_number
FROM users 
WHERE phone_number = '0505979884';
```

