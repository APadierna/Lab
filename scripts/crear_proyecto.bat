@echo off
where python >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Python no encontrado. Instala Python desde https://www.python.org
    pause
    exit /b 1
)
python "%~dp0crear_proyecto.py" %*
pause
