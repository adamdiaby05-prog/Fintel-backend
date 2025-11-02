# Script PowerShell pour générer une SECRET_KEY sécurisée
$bytes = New-Object Byte[](32)
[Security.Cryptography.RandomNumberGenerator]::Create().GetBytes($bytes)
$secretKey = [Convert]::ToBase64String($bytes)
Write-Host "SECRET_KEY=$secretKey" -ForegroundColor Green
Write-Host ""
Write-Host "Copiez cette ligne dans vos variables d'environnement Dokploy !" -ForegroundColor Yellow

