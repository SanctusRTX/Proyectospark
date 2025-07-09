@echo off
setlocal enabledelayedexpansion

:: Título y bienvenida
echo ========================================
echo Preparador de Dependencias Portables
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

:: Crear directorio de dependencias
if not exist dependencies (
    mkdir dependencies
)

:: Generar requirements.txt actualizado
pip freeze > requirements.txt

:: Descargar wheels de todas las dependencias
echo Descargando dependencias...
pip wheel -r requirements.txt -w ./dependencies

echo.
echo ¡Dependencias empaquetadas con éxito!
echo Contenido de la carpeta dependencies:
dir dependencies
pause 