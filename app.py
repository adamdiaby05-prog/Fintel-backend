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
                transaction_type TEXT NOT NULL, -- 'depot', 'retrait', 'envoi', 'reception'
                amount DECIMAL(10,2) NOT NULL,
                currency TEXT DEFAULT 'XOF',
                recipient_phone TEXT,
                sender_phone TEXT,
                status TEXT DEFAULT 'pending', -- 'pending', 'completed', 'failed'
                description TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
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
                is_active BOOLEAN DEFAULT 1,
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
                type TEXT DEFAULT 'info', -- 'info', 'success', 'warning', 'error'
                is_read BOOLEAN DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')
        
        conn.commit()
        conn.close()
        
        # Insérer des données de test
        self.insert_test_data()
    
    def insert_test_data(self):
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        
        # Utilisateur de test
        cursor.execute('''
            INSERT OR IGNORE INTO users (phone_number, password_hash, full_name, email, is_verified)
            VALUES (?, ?, ?, ?, ?)
        ''', ('+2250505979884', hashlib.sha256('azerty'.encode()).hexdigest(), 'Test User', 'test@fintel.com', 1))
        
        # Portefeuille de test
        cursor.execute('SELECT id FROM users WHERE phone_number = ?', ('+2250505979884',))
        user_id = cursor.fetchone()[0]
        
        cursor.execute('''
            INSERT OR IGNORE INTO wallets (user_id, balance, currency)
            VALUES (?, ?, ?)
        ''', (user_id, 50000.00, 'XOF'))
        
        # Partenaires de test
        partners = [
            ('Orange Money', 'https://example.com/orange.png', 'Mobile Money', 'Service de paiement mobile'),
            ('MTN Mobile Money', 'https://example.com/mtn.png', 'Mobile Money', 'Service de paiement mobile'),
            ('Wave', 'https://example.com/wave.png', 'Mobile Money', 'Service de paiement mobile'),
            ('Moov Money', 'https://example.com/moov.png', 'Mobile Money', 'Service de paiement mobile'),
            ('Banque Atlantique', 'https://example.com/atlantique.png', 'Banque', 'Banque traditionnelle'),
            ('Ecobank', 'https://example.com/ecobank.png', 'Banque', 'Banque traditionnelle'),
        ]
        
        for partner in partners:
            cursor.execute('''
                INSERT OR IGNORE INTO partners (name, logo_url, category, description)
                VALUES (?, ?, ?, ?)
            ''', partner)
        
        # Notifications de test
        notifications = [
            (user_id, 'Bienvenue sur Fintel!', 'Votre compte a été créé avec succès.', 'success'),
            (user_id, 'Nouveau partenaire', 'Orange Money est maintenant disponible.', 'info'),
            (user_id, 'Transaction réussie', 'Votre dépôt de 10,000 XOF a été effectué.', 'success'),
        ]
        
        for notif in notifications:
            cursor.execute('''
                INSERT OR IGNORE INTO notifications (user_id, title, message, type)
                VALUES (?, ?, ?, ?)
            ''', notif)
        
        conn.commit()
        conn.close()

class FintelAPIHandler(BaseHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        self.db = DatabaseManager()
        super().__init__(*args, **kwargs)
    
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        self.end_headers()
    
    def do_GET(self):
        path = urlparse(self.path).path
        
        if path == '/health':
            self.send_json_response({"status": "healthy", "message": "API Fintel opérationnelle"})
        
        elif path == '/api/v1/user/profile':
            self.get_user_profile()
        
        elif path == '/api/v1/wallet/balance':
            self.get_wallet_balance()
        
        elif path == '/api/v1/transactions':
            self.get_transactions()
        
        elif path == '/api/v1/partners':
            self.get_partners()
        
        elif path == '/api/v1/notifications':
            self.get_notifications()
        
        else:
            self.send_error(404, "Endpoint not found")
    
    def do_POST(self):
        path = urlparse(self.path).path
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        
        try:
            data = json.loads(post_data.decode('utf-8'))
        except:
            data = {}
        
        if path == '/api/v1/auth/register':
            self.register_user(data)
        
        elif path == '/api/v1/auth/verify-otp':
            self.verify_otp(data)
        
        elif path == '/api/v1/auth/login':
            self.login_user(data)
        
        elif path == '/api/v1/transactions/depot':
            self.create_depot_transaction(data)
        
        elif path == '/api/v1/transactions/retrait':
            self.create_retrait_transaction(data)
        
        elif path == '/api/v1/transactions/envoi':
            self.create_envoi_transaction(data)
        
        elif path == '/api/v1/notifications/mark-read':
            self.mark_notification_read(data)
        
        else:
            self.send_error(404, "Endpoint not found")
    
    def send_json_response(self, data, status_code=200):
        self.send_response(status_code)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps(data, ensure_ascii=False).encode('utf-8'))
    
    def get_user_profile(self):
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute('''
            SELECT phone_number, full_name, email, is_verified, created_at
            FROM users WHERE phone_number = ?
        ''', ('+2250505979884',))
        user = cursor.fetchone()
        conn.close()
        
        if user:
            self.send_json_response({
                "phone_number": user[0],
                "full_name": user[1],
                "email": user[2],
                "is_verified": bool(user[3]),
                "created_at": user[4]
            })
        else:
            self.send_error(404, "User not found")
    
    def get_wallet_balance(self):
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute('''
            SELECT w.balance, w.currency
            FROM wallets w
            JOIN users u ON w.user_id = u.id
            WHERE u.phone_number = ?
        ''', ('+2250505979884',))
        wallet = cursor.fetchone()
        conn.close()
        
        if wallet:
            self.send_json_response({
                "balance": wallet[0],
                "currency": wallet[1]
            })
        else:
            self.send_error(404, "Wallet not found")
    
    def get_transactions(self):
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute('''
            SELECT t.transaction_type, t.amount, t.currency, t.status, t.description, t.created_at
            FROM transactions t
            JOIN users u ON t.user_id = u.id
            WHERE u.phone_number = ?
            ORDER BY t.created_at DESC
            LIMIT 20
        ''', ('+2250505979884',))
        transactions = cursor.fetchall()
        conn.close()
        
        transactions_data = []
        for t in transactions:
            transactions_data.append({
                "type": t[0],
                "amount": t[1],
                "currency": t[2],
                "status": t[3],
                "description": t[4],
                "created_at": t[5]
            })
        
        self.send_json_response({"transactions": transactions_data})
    
    def get_partners(self):
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute('SELECT name, logo_url, category, description FROM partners WHERE is_active = 1')
        partners = cursor.fetchall()
        conn.close()
        
        partners_data = []
        for p in partners:
            partners_data.append({
                "name": p[0],
                "logo_url": p[1],
                "category": p[2],
                "description": p[3]
            })
        
        self.send_json_response({"partners": partners_data})
    
    def get_notifications(self):
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute('''
            SELECT title, message, type, is_read, created_at
            FROM notifications n
            JOIN users u ON n.user_id = u.id
            WHERE u.phone_number = ?
            ORDER BY n.created_at DESC
        ''', ('+2250505979884',))
        notifications = cursor.fetchall()
        conn.close()
        
        notifications_data = []
        for n in notifications:
            notifications_data.append({
                "title": n[0],
                "message": n[1],
                "type": n[2],
                "is_read": bool(n[3]),
                "created_at": n[4]
            })
        
        self.send_json_response({"notifications": notifications_data})
    
    def register_user(self, data):
        phone_number = data.get('phone_number', '')
        self.send_json_response({
            "message": "Utilisateur enregistré avec succès",
            "phone_number": phone_number,
            "otp_code": "1234"
        })
    
    def verify_otp(self, data):
        phone_number = data.get('phone_number', '')
        otp_code = data.get('otp_code', '')
        
        if otp_code == "1234":
            self.send_json_response({
                "message": "OTP vérifié avec succès",
                "phone_number": phone_number,
                "verified": True
            })
        else:
            self.send_json_response({
                "message": "Code OTP incorrect",
                "verified": False
            })
    
    def login_user(self, data):
        phone_number = data.get('phone_number', '')
        password = data.get('password', '')
        
        if password == "azerty":
            self.send_json_response({
                "message": "Connexion réussie",
                "phone_number": phone_number,
                "access_token": "test-token-12345"
            })
        else:
            self.send_json_response({
                "message": "Mot de passe incorrect",
                "verified": False
            })
    
    def create_depot_transaction(self, data):
        amount = data.get('amount', 0)
        
        # Simuler l'ajout de la transaction à la base de données
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute('SELECT id FROM users WHERE phone_number = ?', ('+2250505979884',))
        user_id = cursor.fetchone()[0]
        
        cursor.execute('''
            INSERT INTO transactions (user_id, transaction_type, amount, currency, status, description)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (user_id, 'depot', amount, 'XOF', 'completed', f'Dépôt de {amount} XOF'))
        
        # Mettre à jour le solde du portefeuille
        cursor.execute('''
            UPDATE wallets SET balance = balance + ? WHERE user_id = ?
        ''', (amount, user_id))
        
        conn.commit()
        conn.close()
        
        self.send_json_response({
            "message": "Dépôt effectué avec succès",
            "amount": amount,
            "new_balance": 50000.00 + amount
        })
    
    def create_retrait_transaction(self, data):
        amount = data.get('amount', 0)
        
        self.send_json_response({
            "message": "Retrait effectué avec succès",
            "amount": amount
        })
    
    def create_envoi_transaction(self, data):
        amount = data.get('amount', 0)
        recipient = data.get('recipient_phone', '')
        
        self.send_json_response({
            "message": "Envoi effectué avec succès",
            "amount": amount,
            "recipient": recipient
        })
    
    def mark_notification_read(self, data):
        notification_id = data.get('notification_id', 0)
        
        self.send_json_response({
            "message": "Notification marquée comme lue",
            "notification_id": notification_id
        })

if __name__ == "__main__":
    PORT = 8000
    server = HTTPServer(('0.0.0.0', PORT), FintelAPIHandler)
    print(f"🚀 Serveur Fintel démarré sur le port {PORT}")
    print(f"📱 API disponible sur: http://localhost:{PORT}")
    print(f"💾 Base de données: {DB_FILE}")
    print(f"🔗 Health check: http://localhost:{PORT}/health")
    print("=" * 50)
    
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n🛑 Serveur arrêté")
        server.server_close()

