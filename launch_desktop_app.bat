@echo off
REM R3ÆLƎR Management System Desktop Launcher
REM Launches the standalone desktop application

echo Starting R3ÆLƎR Management System Desktop Application...
echo.

cd /d "%~dp0"

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8+ and add it to your PATH
    pause
    exit /b 1
)

REM Install required packages if needed
echo Checking for required packages...
pip install tk psycopg2-binary requests --quiet

REM Launch the desktop application
echo Launching R3ÆLƎR Desktop Application...
python r3aler_desktop_app.py

pause