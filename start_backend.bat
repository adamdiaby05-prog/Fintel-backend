@echo off
echo ========================================
echo   DEMARRAGE DU BACKEND FINTEL
echo ========================================
echo.

REM Activer l'environnement virtuel
echo Activation de l'environnement virtuel...
call venv\Scripts\activate.bat

REM Vérifier que Python est accessible
python --version
if errorlevel 1 (
    echo ERREUR: Python n'est pas accessible
    pause
    exit /b 1
)

echo.
echo Demarrage du serveur FastAPI...
echo URL: http://192.168.100.7:8000
echo API Docs: http://192.168.100.7:8000/docs
echo.
echo Appuyez sur Ctrl+C pour arreter le serveur
echo.

REM Démarrer le serveur
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

pause
