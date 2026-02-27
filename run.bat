@echo off
title AGMS Enterprise
echo.
echo  ================================================================
echo   AGMS Enterprise — AG Multi Services Business OS
echo   Starting...
echo  ================================================================
echo.

:: Check Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo  [ERROR] Python not found!
    echo  Please install Python 3.11 from https://python.org/downloads/
    echo  IMPORTANT: Check "Add Python to PATH" during install!
    pause
    exit /b 1
)

:: Check Python version
for /f "tokens=2 delims= " %%v in ('python --version 2^>^&1') do set PYVER=%%v
echo  Python: %PYVER%

:: Create venv if not exists
if not exist ".venv" (
    echo  [SETUP] Creating virtual environment...
    python -m venv .venv
)

:: Activate venv
call .venv\Scripts\activate.bat

:: Install/update packages
echo  [SETUP] Checking dependencies...
python -m pip install --quiet --upgrade pip
python -m pip install --quiet PySide6 cryptography Pillow requests 2>nul
python -m pip install --quiet reportlab openpyxl 2>nul
python -m pip install --quiet bcrypt PyJWT psutil schedule qrcode 2>nul

:: Check if main packages ok
python -c "import PySide6; import cryptography" >nul 2>&1
if %errorlevel% neq 0 (
    echo  [ERROR] Core packages install failed!
    echo  Run manually: pip install PySide6 cryptography Pillow requests
    pause
    exit /b 1
)

:: Launch app
echo  [START] Launching AGMS Enterprise...
echo.
python launcher.py

if %errorlevel% neq 0 (
    echo.
    echo  [ERROR] App crashed! Check error above.
    pause
)
