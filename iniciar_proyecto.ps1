# Script de inicio del Proyecto Educativo

# Configurar colores y estilo de la consola
$host.UI.RawUI.BackgroundColor = "Black"
$host.UI.RawUI.ForegroundColor = "Green"
Clear-Host

# Función para mostrar mensaje de error
function Show-ErrorMessage {
    param([string]$Message)
    Write-Host "`n[ERROR] $Message" -ForegroundColor Red
    Write-Host "Por favor, contacta al soporte técnico." -ForegroundColor Yellow
    Read-Host "Presiona Enter para salir"
    exit 1
}

# Mensaje de bienvenida
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "   INICIANDO PROYECTO EDUCATIVO" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan

# Cambiar al directorio del proyecto
try {
    $scriptPath = Split-Path -Parent $MyInvocation.MyCommand.Definition
    Set-Location $scriptPath
} catch {
    Show-ErrorMessage "No se pudo cambiar al directorio del proyecto."
}

# Verificar existencia del entorno virtual
if (-not (Test-Path "env\Scripts\Activate.ps1")) {
    Show-ErrorMessage "No se encontró el entorno virtual. Ejecuta setup_environment.ps1 primero."
}

# Activar entorno virtual
try {
    . .\env\Scripts\Activate.ps1
} catch {
    Show-ErrorMessage "Error al activar el entorno virtual."
}

# Cambiar al directorio src
try {
    Set-Location src
} catch {
    Show-ErrorMessage "No se pudo cambiar al directorio src."
}

# Ejecutar la aplicación
try {
    Write-Host "`nIniciando servidor..." -ForegroundColor Green
    python app.py
} catch {
    Show-ErrorMessage "Error al iniciar la aplicación. Verifica la instalación de Python y las dependencias."
}

# Mensaje de finalización
Write-Host "`n¡Servidor detenido!" -ForegroundColor Yellow
Read-Host "Presiona Enter para salir" 