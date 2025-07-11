@echo off
title Proyecto Educativo - Iniciar Servidor
color 0A

echo ========================================
echo   INICIANDO PROYECTO EDUCATIVO
echo ========================================

:: Cambiar al directorio del proyecto
cd /d "%~dp0"

:: Verificar si el entorno virtual existe
if not exist "env\Scripts\activate.bat" (
    echo Error: No se encontró el entorno virtual.
    echo Por favor, ejecuta setup_environment.ps1 primero.
    pause
    exit /b 1
)

:: Activar entorno virtual
call env\Scripts\activate

:: Cambiar al directorio src
cd src

:: Ejecutar la aplicación
python app.py

:: Mantener la ventana abierta si hay un error
if %errorlevel% neq 0 (
    echo.
    echo ¡Ocurrió un error al iniciar la aplicación!
    echo Revisa los mensajes anteriores para más detalles.
    pause
)

:: Desactivar entorno virtual
deactivate

pause 