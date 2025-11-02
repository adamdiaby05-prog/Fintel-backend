# Script de test PowerShell pour Windows
Write-Host "========================================"
Write-Host "  TEST DE SAUVEGARDE DES DONNÉES"
Write-Host "========================================"
Write-Host ""

# Vérifier si requests est installé
try {
    python -c "import requests" 2>$null
    Write-Host "✅ requests est installé" -ForegroundColor Green
} catch {
    Write-Host "❌ requests n'est pas installé. Installation..." -ForegroundColor Yellow
    pip install requests
}

Write-Host ""
Write-Host "Lancement des tests..." -ForegroundColor Cyan
Write-Host ""

# Exécuter le script Python
python test_user_profile.py

Write-Host ""
Write-Host "========================================"
Write-Host "  FIN DES TESTS"
Write-Host "========================================"

