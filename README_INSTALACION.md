# Guía de Instalación Portable

## Requisitos Previos
- Python 3.8 o superior
- Windows 10/11
- Permisos de administrador

## Pasos de Instalación

### Método 1: Instalación Automática
1. Ejecuta `install_dependencies.bat`
2. Sigue las instrucciones en pantalla

### Método 2: Instalación Manual
1. Crea un entorno virtual:
   ```
   python -m venv env
   ```

2. Activa el entorno virtual:
   ```
   env\Scripts\activate
   ```

3. Instala dependencias:
   ```
   pip install --no-index --find-links=.\dependencies -r requirements.txt
   ```

## Solución de Problemas
- Asegúrate de tener Python instalado
- Verifica que tienes permisos de ejecución
- Comprueba la compatibilidad de versiones de Python

## Ejecución del Proyecto
Después de instalar dependencias:
```
cd src
python app.py
```

## Notas Importantes
- Los scripts son específicos para Windows
- Requiere Python 3.8+
- Las dependencias son específicas de tu arquitectura de sistema 