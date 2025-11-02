#!/usr/bin/env python3
import json
import sqlite3
from datetime import datetime, timedelta
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import hashlib
import secrets

# Configuration de la base de données
DB_FILE = 'fintel.db'

class DatabaseManager:
    def __init__(self):
        self.init_database()
        self.seed_data()
    
    def init_database(self):
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        
        # Table des utilisateurs
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                phone_number TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                full_name TEXT,
                email TEXT,
                is_active BOOLEAN DEFAULT 1,
                is_verified BOOLEAN DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Table des portefeuilles
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS wallets (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                balance DECIMAL(10,2) DEFAULT 0.00,
                currency TEXT DEFAULT 'XOF',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')
        
        # Table des transactions
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS transactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                type TEXT NOT NULL,
                amount DECIMAL(10,2) NOT NULL,
                currency TEXT DEFAULT 'XOF',
                status TEXT DEFAULT 'completed',
                description TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')
        
        # Table des partenaires
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS partners (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                logo_url TEXT,
                category TEXT,
                description TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Table des notifications
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS notifications (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                title TEXT NOT NULL,
                message TEXT NOT NULL,
                type TEXT DEFAULT 'info',
                is_read BOOLEAN DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')

        # Table d'état applicatif simple (clé/valeur)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS app_state (
                key TEXT PRIMARY KEY,
                value TEXT
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def seed_data(self):
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        
        # Vérifier si les données existent déjà
        cursor.execute('SELECT COUNT(*) FROM users')
        if cursor.fetchone()[0] > 0:
            conn.close()
            return
        
        # Créer l'utilisateur avec votre nom
        password_hash = hashlib.sha256("azerty".encode()).hexdigest()
        cursor.execute('''
            INSERT INTO users (phone_number, password_hash, full_name, email, is_active, is_verified)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', ("+2250505979884", password_hash, "Junior Lobé", "junior.lobe@fintel.com", 1, 1))
        
        user_id = cursor.lastrowid
        
        # Créer le portefeuille (solde initial à 0 pour un nouvel utilisateur)
        cursor.execute('''
            INSERT INTO wallets (user_id, balance, currency)
            VALUES (?, ?, ?)
        ''', (user_id, 0.00, "XOF"))
        
        # Ne pas créer de transactions par défaut pour un nouvel utilisateur
        
        # Créer des partenaires
        partners = [
            ("Orange Money", "https://example.com/orange.png", "Mobile Money", "Service de paiement mobile Orange"),
            ("MTN Mobile Money", "https://example.com/mtn.png", "Mobile Money", "Service de paiement mobile MTN"),
            ("Wave", "https://example.com/wave.png", "Mobile Money", "Service de paiement mobile Wave"),
            ("Ecobank", "https://example.com/ecobank.png", "Banque", "Banque panafricaine"),
            ("BOA", "https://example.com/boa.png", "Banque", "Bank of Africa"),
        ]
        
        for partner in partners:
            cursor.execute('''
                INSERT INTO partners (name, logo_url, category, description)
                VALUES (?, ?, ?, ?)
            ''', partner)
        
        # Créer des notifications
        notifications = [
            (user_id, "Bienvenue sur Fintel!", "Votre compte a été créé avec succès.", "success"),
        ]
        
        for notification in notifications:
            cursor.execute('''
                INSERT INTO notifications (user_id, title, message, type, is_read)
                VALUES (?, ?, ?, ?, ?)
            ''', (*notification, 0))
        
        conn.commit()
        conn.close()
        print("Base de données initialisée avec vos données personnelles!")

class FintelAPIHandler(BaseHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        self.db = DatabaseManager()
        super().__init__(*args, **kwargs)

    # --- Helpers état ---
    def normalize_phone(self, phone: str | None) -> str | None:
        if not phone:
            return None
        digits = ''.join(ch for ch in phone if ch.isdigit())
        if len(digits) >= 10:
            local = digits[-10:]
        else:
            local = digits
        # retourne format +225XXXXXXXXXX
        if digits.startswith('225') and len(digits) > 10:
            return '+' + digits
        return '+225' + local if not phone.startswith('+') else '+' + digits
    def set_last_phone(self, phone: str):
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute('INSERT OR REPLACE INTO app_state(key, value) VALUES (?, ?)', ('last_phone', phone))
        conn.commit()
        conn.close()

    def get_last_phone(self) -> str | None:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute('SELECT value FROM app_state WHERE key = ?', ('last_phone',))
        row = cursor.fetchone()
        conn.close()
        return row[0] if row else None
    
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        self.end_headers()
    
    def do_GET(self):
        parsed_path = urlparse(self.path)
        path = parsed_path.path
        query = parse_qs(parsed_path.query)
        phone = self.normalize_phone(query.get('phone', [None])[0])
        
        # Headers CORS
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        
        if path == '/health':
            response = {"status": "healthy", "message": "API Fintel opérationnelle"}
        elif path == '/api/v1/user/profile':
            response = self.get_user_profile(phone)
        elif path == '/api/v1/wallet/balance':
            response = self.get_wallet_balance(phone)
        elif path == '/api/v1/transactions':
            response = self.get_transactions(phone)
        elif path == '/api/v1/partners':
            response = self.get_partners()
        elif path == '/api/v1/notifications':
            response = self.get_notifications(phone)
        elif path == '/api/v1/debug/dump':
            response = self.dump_all()
        else:
            response = {"error": "Endpoint non trouvé"}
        
        self.wfile.write(json.dumps(response, ensure_ascii=False).encode('utf-8'))
    
    def do_POST(self):
        parsed_path = urlparse(self.path)
        path = parsed_path.path
        
        # Lire le body de la requête
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        
        try:
            data = json.loads(post_data.decode('utf-8'))
        except:
            data = {}
        
        # Headers CORS
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        
        if path == '/api/v1/auth/register':
            response = self.register_user(data)
        elif path == '/api/v1/auth/verify-otp':
            response = self.verify_otp(data)
        elif path == '/api/v1/auth/login':
            response = self.login_user(data)
        elif path == '/api/v1/transactions/depot':
            response = self.create_depot(data)
        elif path == '/api/v1/transactions/retrait':
            response = self.create_retrait(data)
        elif path == '/api/v1/transactions/envoi':
            response = self.create_envoi(data)
        elif path == '/api/v1/notifications/mark-read':
            response = self.mark_notification_read(data)
        elif path == '/api/v1/user/profile/update':
            response = self.update_user_profile(data)
        else:
            response = {"error": "Endpoint non trouvé"}
        
        self.wfile.write(json.dumps(response, ensure_ascii=False).encode('utf-8'))
    
    def get_user_profile(self, phone: str | None):
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        if not phone:
            phone = self.get_last_phone()
        phone = self.normalize_phone(phone)
        cursor.execute('''
            SELECT phone_number, full_name, email, is_verified, created_at
            FROM users WHERE phone_number = ?
        ''', (phone or "+2250505979884",))
        
        user = cursor.fetchone()
        conn.close()
        
        if user:
            return {
                "phone_number": user[0],
                "full_name": user[1],
                "email": user[2],
                "is_verified": bool(user[3]),
                "created_at": user[4]
            }
        return {"error": "Utilisateur non trouvé"}

    def update_user_profile(self, data):
        full_name = data.get('full_name', '').strip()
        phone = self.normalize_phone(data.get('phone', ''))
        if not full_name:
            return {"error": "full_name requis"}
        if not phone:
            phone = self.get_last_phone()
            phone = self.normalize_phone(phone)
        if not phone:
            return {"error": "phone requis"}
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE users SET full_name = ?, updated_at = CURRENT_TIMESTAMP
            WHERE phone_number = ?
        ''', (full_name, phone,))
        conn.commit()
        conn.close()
        self.set_last_phone(phone)
        return {"message": "Profil mis à jour", "full_name": full_name}
    
    def get_wallet_balance(self, phone: str | None):
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        if not phone:
            phone = self.get_last_phone()
        phone = self.normalize_phone(phone)
        
        cursor.execute('''
            SELECT w.balance, w.currency
            FROM wallets w
            JOIN users u ON w.user_id = u.id
            WHERE u.phone_number = ?
        ''', ((phone or "+2250505979884"),))
        
        wallet = cursor.fetchone()
        conn.close()
        
        if wallet:
            return {
                "balance": wallet[0],
                "currency": wallet[1]
            }
        return {"error": "Portefeuille non trouvé"}
    
    def get_transactions(self, phone: str | None):
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        if not phone:
            phone = self.get_last_phone()
        phone = self.normalize_phone(phone)
        
        cursor.execute('''
            SELECT t.type, t.amount, t.currency, t.status, t.description, t.created_at
            FROM transactions t
            JOIN users u ON t.user_id = u.id
            WHERE u.phone_number = ?
            ORDER BY t.created_at DESC
        ''', ((phone or "+2250505979884"),))
        
        transactions = cursor.fetchall()
        conn.close()
        
        return {
            "transactions": [
                {
                    "type": t[0],
                    "amount": t[1],
                    "currency": t[2],
                    "status": t[3],
                    "description": t[4],
                    "created_at": t[5]
                }
                for t in transactions
            ]
        }
    
    def get_partners(self):
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        
        cursor.execute('SELECT name, logo_url, category, description FROM partners')
        partners = cursor.fetchall()
        conn.close()
        
        return {
            "partners": [
                {
                    "name": p[0],
                    "logo_url": p[1],
                    "category": p[2],
                    "description": p[3]
                }
                for p in partners
            ]
        }
    
    def get_notifications(self, phone: str | None):
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        if not phone:
            phone = self.get_last_phone()
        phone = self.normalize_phone(phone)
        
        cursor.execute('''
            SELECT n.title, n.message, n.type, n.is_read, n.created_at
            FROM notifications n
            JOIN users u ON n.user_id = u.id
            WHERE u.phone_number = ?
            ORDER BY n.created_at DESC
        ''', ((phone or "+2250505979884"),))

    def dump_all(self):
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute('SELECT id, phone_number, full_name, email, is_verified, created_at FROM users')
        users = cursor.fetchall()
        cursor.execute('SELECT id, user_id, balance, currency, created_at FROM wallets')
        wallets = cursor.fetchall()
        cursor.execute('SELECT id, user_id, type, amount, currency, status, description, created_at FROM transactions')
        transactions = cursor.fetchall()
        cursor.execute('SELECT id, user_id, title, message, type, is_read, created_at FROM notifications')
        notifications = cursor.fetchall()
        cursor.execute('SELECT key, value FROM app_state')
        app_state = cursor.fetchall()
        conn.close()
        return {
            "users": users,
            "wallets": wallets,
            "transactions": transactions,
            "notifications": notifications,
            "app_state": app_state,
        }
        
        notifications = cursor.fetchall()
        conn.close()
        
        return {
            "notifications": [
                {
                    "title": n[0],
                    "message": n[1],
                    "type": n[2],
                    "is_read": bool(n[3]),
                    "created_at": n[4]
                }
                for n in notifications
            ]
        }
    
    def register_user(self, data):
        phone_number = self.normalize_phone(data.get('phone_number', '').strip())
        if not phone_number:
            return {"error": "phone_number requis"}
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute('SELECT id FROM users WHERE phone_number = ?', (phone_number,))
        exists = cursor.fetchone()
        if exists:
            conn.close()
            return {"error": "Numéro déjà enregistré"}
        password_hash = hashlib.sha256("azerty".encode()).hexdigest()
        cursor.execute('''
            INSERT INTO users (phone_number, password_hash, full_name, is_active, is_verified)
            VALUES (?, ?, ?, 1, 1)
        ''', (phone_number, password_hash, None))
        user_id = cursor.lastrowid
        cursor.execute('INSERT INTO wallets (user_id, balance, currency) VALUES (?, ?, ?)', (user_id, 0.00, 'XOF'))
        conn.commit()
        conn.close()
        self.set_last_phone(phone_number)
        return {"message": "Utilisateur enregistré avec succès", "phone_number": phone_number, "otp_code": "1234"}
    
    def verify_otp(self, data):
        phone_number = data.get('phone_number', '')
        otp_code = data.get('otp_code', '')
        
        if otp_code == "1234":
            return {
                "message": "OTP vérifié avec succès",
                "phone_number": phone_number,
                "verified": True
            }
        
        return {
            "message": "Code OTP incorrect",
            "verified": False
        }
    
    def login_user(self, data):
        phone_number = self.normalize_phone(data.get('phone_number', ''))
        password = data.get('password', '')
        
        if password == "azerty":
            # S'assurer que l'utilisateur existe
            conn = sqlite3.connect(DB_FILE)
            cursor = conn.cursor()
            cursor.execute('SELECT id FROM users WHERE phone_number = ?', (phone_number,))
            row = cursor.fetchone()
            if not row:
                # auto-create minimal user if not existing
                password_hash = hashlib.sha256("azerty".encode()).hexdigest()
                cursor.execute('INSERT INTO users (phone_number, password_hash, is_active, is_verified) VALUES (?, ?, 1, 1)', (phone_number, password_hash))
                user_id = cursor.lastrowid
                cursor.execute('INSERT INTO wallets (user_id, balance, currency) VALUES (?, ?, ?)', (user_id, 0.00, 'XOF'))
                conn.commit()
            conn.close()
            self.set_last_phone(phone_number)
            return {
                "message": "Connexion réussie",
                "phone_number": phone_number,
                "access_token": "test-token-12345"
            }
        
        return {
            "message": "Mot de passe incorrect",
            "verified": False
        }
    
    def create_depot(self, data):
        amount = data.get('amount', 0)
        return {
            "message": "Dépôt effectué avec succès",
            "amount": amount,
            "new_balance": 50000.00 + amount
        }
    
    def create_retrait(self, data):
        amount = data.get('amount', 0)
        return {
            "message": "Retrait effectué avec succès",
            "amount": amount
        }
    
    def create_envoi(self, data):
        amount = data.get('amount', 0)
        recipient = data.get('recipient_phone', '')
        return {
            "message": "Envoi effectué avec succès",
            "amount": amount,
            "recipient": recipient
        }
    
    def mark_notification_read(self, data):
        notification_id = data.get('notification_id', 0)
        return {
            "message": "Notification marquée comme lue",
            "notification_id": notification_id
        }

if __name__ == '__main__':
    server = HTTPServer(('0.0.0.0', 8000), FintelAPIHandler)
    # Avoid non-ASCII in console to prevent UnicodeEncodeError on Windows
    print("Serveur Fintel API demarre sur http://0.0.0.0:8000")
    print("Utilisateur 'Junior Lobe' initialise dans la base de donnees")
    print("API disponible sur http://localhost:8000")
    print("Healthcheck: http://localhost:8000/health")
    server.serve_forever()

