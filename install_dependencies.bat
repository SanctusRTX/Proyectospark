@echo off
setlocal enabledelayedexpansion

:: Título y bienvenida
echo ========================================
echo Instalador Portable de Dependencias
echo Proyecto Educativo Flask
echo ========================================

:: Verificar Python
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python no está instalado.
    echo Por favor, instala Python 3.8 o superior.
    pause
    exit /b 1
)

:: Crear entorno virtual si no existe
if not exist env\ (
    echo Creando entorno virtual...
    python -m venv env
)

:: Activar entorno virtual
call env\Scripts\activate

:: Instalar dependencias desde wheels
echo Instalando dependencias...
pip install --no-index --find-links=.\dependencies -r requirements.txt

:: Verificar instalación
echo Verificando instalación de dependencias...
pip list

echo.
echo ¡Instalación completada con éxito!
echo Puedes activar el entorno virtual con:
echo env\Scripts\activate
pause 