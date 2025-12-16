@echo off
REM R3ÆLƎR AI - Start Enhanced Intelligence Layer
REM This script starts the Enhanced Knowledge API (port 5010)
REM DOES NOT MODIFY DATABASE - only adds intelligence wrapper

echo ============================================================
echo R3AELER AI - Enhanced Intelligence Layer Startup
echo ============================================================
echo.

REM Check if Storage Facility is running
echo [1/4] Checking Storage Facility (port 5003)...
curl -s http://localhost:5003/api/facility/health > nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Storage Facility not running on port 5003
    echo Please start Storage Facility first:
    echo   python AI_Core_Worker\storage_facility.py
    echo.
    pause
    exit /b 1
)
echo [OK] Storage Facility is running

REM Check if Knowledge API is running (optional but recommended)
echo [2/4] Checking Knowledge API (port 5001)...
curl -s http://localhost:5001/api/kb/health > nul 2>&1
if %errorlevel% neq 0 (
    echo [WARNING] Knowledge API not running on port 5001
    echo This is optional but recommended for full functionality
) else (
    echo [OK] Knowledge API is running
)

REM Check dependencies
echo [3/4] Checking Python dependencies...
python -c "import requests, flask, flask_cors" 2> nul
if %errorlevel% neq 0 (
    echo [ERROR] Missing dependencies. Installing...
    pip install requests flask flask-cors
    if %errorlevel% neq 0 (
        echo [ERROR] Failed to install dependencies
        pause
        exit /b 1
    )
)
echo [OK] All dependencies installed

REM Start Enhanced Knowledge API
echo [4/4] Starting Enhanced Knowledge API (port 5010)...
echo.
echo ============================================================
echo READY TO LAUNCH
echo ============================================================
echo.
echo Features enabled:
echo   - Intent Classification (7 types)
echo   - Live External Data (CoinGecko, NIST NVD, Wikipedia)
echo   - Circuit Breakers (reliability)
echo   - Security Validation (SQL injection, XSS, rate limiting)
echo   - Performance Monitoring (metrics, uptime)
echo   - Emergency Kill Switch
echo.
echo Database Status: PRESERVED (no modifications)
echo.
echo Starting in 3 seconds...
timeout /t 3 /nobreak > nul
echo.

cd AI_Core_Worker
python enhanced_knowledge_api.py

REM If the script exits, show error
echo.
echo [ERROR] Enhanced API stopped unexpectedly
pause
