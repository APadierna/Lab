@echo off

:: Intentar con el Python Launcher (py), luego python, luego python3
set PYTHON_CMD=

where py >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    set PYTHON_CMD=py
    goto run
)

:: "where python" devuelve ok incluso cuando apunta al alias de la Store,
:: así que verificamos que realmente ejecuta algo útil
python -c "import sys" >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    set PYTHON_CMD=python
    goto run
)

where python3 >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    set PYTHON_CMD=python3
    goto run
)

echo [ERROR] Python no encontrado.
echo         Instala Python desde https://www.python.org
echo         o desactiva el alias en: Configuracion ^> Apps ^> Alias de ejecucion de aplicaciones
pause
exit /b 1

:run
%PYTHON_CMD% "%~dp0crear_proyecto.py" %*
pause
