@echo off

set PYTHON_CMD=

where py >nul 2>&1
if %ERRORLEVEL% EQU 0 ( set PYTHON_CMD=py & goto run )

python -c "import sys" >nul 2>&1
if %ERRORLEVEL% EQU 0 ( set PYTHON_CMD=python & goto run )

where python3 >nul 2>&1
if %ERRORLEVEL% EQU 0 ( set PYTHON_CMD=python3 & goto run )

echo [ERROR] Python no encontrado.
echo         Instala Python desde https://www.python.org
pause
exit /b 1

:run
%PYTHON_CMD% "%~dp0generar_entrega.py" %*
pause
