# Script de configuración de entorno virtual y desbloqueo de ejecución de scripts

# Función para verificar y solicitar permisos de administrador
function Request-AdminPrivileges {
    $currentUser = [Security.Principal.WindowsIdentity]::GetCurrent()
    $principal = New-Object Security.Principal.WindowsPrincipal($currentUser)
    
    if (-not $principal.IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)) {
        Write-Host "Este script requiere permisos de administrador. Por favor, ejecuta como administrador."
        pause
        exit
    }
}

# Verificar permisos de administrador
Request-AdminPrivileges

# Desbloquear la ejecución de scripts de PowerShell
Write-Host "Desbloqueando la ejecución de scripts de PowerShell..."
Set-ExecutionPolicy RemoteSigned -Force

# Verificar si Python está instalado
$pythonVersion = python --version 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Host "Python no está instalado. Por favor, instala Python 3.8 o superior."
    pause
    exit
}

# Cambiar al directorio del proyecto
$projectPath = Split-Path -Parent $PSCommandPath
Set-Location $projectPath

# Crear entorno virtual
Write-Host "Creando entorno virtual..."
python -m venv env

# Activar entorno virtual
.\env\Scripts\Activate

# Instalar dependencias
Write-Host "Instalando dependencias..."
pip install --no-index --find-links=..\dependencies -r ..\requirements.txt

Write-Host "Configuración completada exitosamente."
pause 