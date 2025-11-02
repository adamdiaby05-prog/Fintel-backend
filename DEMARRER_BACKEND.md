# 🚀 Démarrer le Backend - Instructions

## ✅ Solution : Utiliser l'Environnement Virtuel

Le projet a déjà un environnement virtuel Python (`venv`). Il faut l'activer avant de démarrer le serveur.

### Option 1 : Utiliser le script batch (RECOMMANDÉ pour Windows)

Double-cliquez sur :
```
Fintel-backend\start_backend.bat
```

OU dans PowerShell/CMD :
```bash
cd C:\Users\ROG\Documents\fintel\Fintel-backend
start_backend.bat
```

### Option 2 : Activer manuellement l'environnement virtuel

**Dans CMD (Invite de commandes)** :
```cmd
cd C:\Users\ROG\Documents\fintel\Fintel-backend
venv\Scripts\activate.bat
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**Dans PowerShell** :
```powershell
cd C:\Users\ROG\Documents\fintel\Fintel-backend
venv\Scripts\Activate.ps1
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Option 3 : Utiliser directement l'exécutable Python du venv

```cmd
cd C:\Users\ROG\Documents\fintel\Fintel-backend
venv\Scripts\python.exe -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## ✅ Vérifier que le serveur démarre

Vous devriez voir :
```
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     Started reloader process
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

## 🌐 Accéder à l'API

- **API principale** : http://192.168.100.7:8000
- **Documentation Swagger** : http://192.168.100.7:8000/docs
- **Health Check** : http://192.168.100.7:8000/health

## ⚠️ Si vous avez une erreur PowerShell

Si PowerShell bloque l'exécution de scripts, exécutez :
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

Puis réessayez d'activer l'environnement virtuel.

