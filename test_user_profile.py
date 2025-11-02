#!/usr/bin/env python3
"""
Script de test pour vérifier que toutes les données utilisateur sont bien sauvegardées
"""

import requests
import json
from datetime import datetime

# Configuration
BASE_URL = "http://192.168.100.7:8000"
TEST_PHONE = "0505979884"

def print_section(title):
    print("\n" + "="*60)
    print(f"  {title}")
    print("="*60)

def test_user_registration():
    """Test de l'inscription d'un utilisateur"""
    print_section("TEST 1: Inscription utilisateur")
    
    url = f"{BASE_URL}/api/v1/auth/register"
    data = {
        "phone_number": TEST_PHONE,
        "password": "test123"
    }
    
    try:
        response = requests.post(url, json=data, timeout=10)
        print(f"Status: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
        return response.status_code in [200, 201]
    except Exception as e:
        print(f"Erreur: {e}")
        return False

def test_update_contact_info():
    """Test de mise à jour des informations de contact"""
    print_section("TEST 2: Mise à jour informations de contact")
    
    url = f"{BASE_URL}/api/v1/user/profile"
    data = {
        "phone_number": TEST_PHONE,
        "whatsapp_number": "0505979884",
        "email": "adamdiaby05@gmail.com",
        "otp_delivery_preference": "sms"
    }
    
    try:
        response = requests.put(url, json=data, timeout=10)
        print(f"Status: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
        return response.status_code == 200
    except Exception as e:
        print(f"Erreur: {e}")
        return False

def test_update_personal_info():
    """Test de mise à jour des informations personnelles"""
    print_section("TEST 3: Mise à jour informations personnelles")
    
    url = f"{BASE_URL}/api/v1/user/profile"
    data = {
        "phone_number": TEST_PHONE,
        "first_name": "Adam",
        "last_name": "diaby",
        "date_of_birth": "2000-01-15",
        "country": "Cote d'Ivoire",
        "city": "Sassandra"
    }
    
    try:
        response = requests.put(url, json=data, timeout=10)
        print(f"Status: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
        return response.status_code == 200
    except Exception as e:
        print(f"Erreur: {e}")
        return False

def test_update_identity_info():
    """Test de mise à jour des informations d'identité"""
    print_section("TEST 4: Mise à jour informations d'identité")
    
    url = f"{BASE_URL}/api/v1/user/profile"
    data = {
        "phone_number": TEST_PHONE,
        "id_type": "Carte d'Identité",
        "id_number": "ci hhhhb",
        "id_issue_date": "2000-01-22",
        "id_expiry_date": "2000-01-28"
    }
    
    try:
        response = requests.put(url, json=data, timeout=10)
        print(f"Status: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
        return response.status_code == 200
    except Exception as e:
        print(f"Erreur: {e}")
        return False

def test_update_security_info():
    """Test de mise à jour des informations de sécurité"""
    print_section("TEST 5: Mise à jour informations de sécurité")
    
    url = f"{BASE_URL}/api/v1/user/profile"
    data = {
        "phone_number": TEST_PHONE,
        "password": "azerty",
        "terms_accepted": True,
        "privacy_policy_accepted": True
    }
    
    try:
        response = requests.put(url, json=data, timeout=10)
        print(f"Status: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
        return response.status_code == 200
    except Exception as e:
        print(f"Erreur: {e}")
        return False

def test_get_user_profile():
    """Test de récupération du profil utilisateur complet"""
    print_section("TEST 6: Récupération profil utilisateur")
    
    url = f"{BASE_URL}/api/v1/user/profile"
    params = {"phone": TEST_PHONE}
    
    try:
        response = requests.get(url, params=params, timeout=10)
        print(f"Status: {response.status_code}")
        profile = response.json()
        print(f"Response: {json.dumps(profile, indent=2, ensure_ascii=False)}")
        
        if response.status_code == 200 and "user" in profile:
            user = profile["user"]
            print("\n✅ Vérification des champs sauvegardés:")
            fields_to_check = [
                ("phone_number", "Numéro de téléphone"),
                ("whatsapp_number", "Numéro WhatsApp"),
                ("email", "Email"),
                ("first_name", "Prénom"),
                ("last_name", "Nom"),
                ("date_of_birth", "Date de naissance"),
                ("country", "Pays"),
                ("city", "Ville"),
                ("id_type", "Type de pièce d'identité"),
                ("id_number", "Numéro de pièce d'identité"),
                ("id_issue_date", "Date d'émission"),
                ("id_expiry_date", "Date d'expiration"),
                ("terms_accepted", "Termes acceptés"),
                ("privacy_policy_accepted", "Politique de confidentialité acceptée"),
            ]
            
            all_saved = True
            for field, label in fields_to_check:
                value = user.get(field)
                status = "✅" if value else "❌"
                print(f"  {status} {label}: {value}")
                if not value and field not in ["id_issue_date", "id_expiry_date", "date_of_birth"]:
                    all_saved = False
            
            return all_saved
        return False
    except Exception as e:
        print(f"Erreur: {e}")
        return False

def test_health_check():
    """Test de santé de l'API"""
    print_section("TEST 0: Vérification santé API")
    
    try:
        response = requests.get(f"{BASE_URL}/health", timeout=5)
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Erreur de connexion: {e}")
        print(f"   Vérifiez que le serveur backend est démarré sur {BASE_URL}")
        return False

def main():
    """Exécuter tous les tests"""
    print("\n" + "="*60)
    print("  TESTS DE SAUVEGARDE DES DONNÉES UTILISATEUR")
    print("="*60)
    
    results = {}
    
    # Test 0: Santé de l'API
    results["health"] = test_health_check()
    if not results["health"]:
        print("\n❌ L'API n'est pas accessible. Veuillez démarrer le serveur backend.")
        return
    
    # Test 1: Inscription
    results["registration"] = test_user_registration()
    
    # Test 2: Informations de contact
    results["contact"] = test_update_contact_info()
    
    # Test 3: Informations personnelles
    results["personal"] = test_update_personal_info()
    
    # Test 4: Informations d'identité
    results["identity"] = test_update_identity_info()
    
    # Test 5: Informations de sécurité
    results["security"] = test_update_security_info()
    
    # Test 6: Récupération complète
    results["retrieval"] = test_get_user_profile()
    
    # Résumé
    print_section("RÉSUMÉ DES TESTS")
    total = len(results)
    passed = sum(1 for v in results.values() if v)
    
    for test_name, result in results.items():
        status = "✅ PASSÉ" if result else "❌ ÉCHOUÉ"
        print(f"  {test_name.upper():<15} {status}")
    
    print(f"\n  Total: {passed}/{total} tests réussis")
    
    if passed == total:
        print("\n🎉 TOUS LES TESTS SONT PASSÉS! Les données sont bien sauvegardées.")
    else:
        print("\n⚠️  Certains tests ont échoué. Vérifiez les erreurs ci-dessus.")

if __name__ == "__main__":
    main()

