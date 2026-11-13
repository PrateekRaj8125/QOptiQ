@echo off
setlocal
title QOptiQ Backend Setup and Launcher
cd /d "%~dp0"

echo ========================================
echo       QOptiQ Backend Setup
echo ========================================
echo.

where python >nul 2>nul
if errorlevel 1 (
    echo ERROR: Python was not found in PATH.
    echo Enable the Python App Execution Aliases or add Python to PATH,
    echo then reopen this file.
    echo You can also test: py -3.13 --version
    pause
    exit /b 1
)

echo [1/5] Creating virtual environment...
if not exist ".venv\Scripts\python.exe" (
    python -m venv .venv
    if errorlevel 1 (
        echo ERROR: Could not create the virtual environment.
        pause
        exit /b 1
    )
) else (
    echo Existing virtual environment found; reusing it.
)

echo.
echo [2/5] Activating virtual environment...
call ".venv\Scripts\activate.bat"
if errorlevel 1 (
    echo ERROR: Could not activate the virtual environment.
    pause
    exit /b 1
)

echo.
echo [3/5] Upgrading pip...
".venv\Scripts\python.exe" -m pip install --upgrade pip
if errorlevel 1 (
    echo ERROR: pip upgrade failed.
    pause
    exit /b 1
)

echo.
echo [4/5] Installing requirements...
".venv\Scripts\python.exe" -m pip install -r requirements.txt
if errorlevel 1 (
    echo ERROR: Dependency installation failed.
    pause
    exit /b 1
)

echo.
echo [5/5] Starting QOptiQ backend...
echo API documentation: http://127.0.0.1:8000/docs
echo Press Ctrl+C to stop the server.
echo.
".venv\Scripts\python.exe" -m uvicorn app.main:app --reload

echo.
echo Backend process ended.
pause
endlocal
