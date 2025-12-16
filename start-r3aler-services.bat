@echo off
echo ============================================================
echo R3ALER AI - Complete System Startup
echo ============================================================
echo.

REM Change to project root directory
cd /d "c:\Users\work8\OneDrive\Desktop\r3al3rai\New Folder 1\R3al3r-AI Main Working\R3aler-ai\R3aler-ai"

REM Start Knowledge API in new window
echo [1/3] Starting Knowledge Base API (Port 5001)...
start "R3ALER - Knowledge API" cmd /k "cd AI_Core_Worker && call ..\blackarch_venv\Scripts\activate.bat && python knowledge_api.py"
timeout /t 3 /nobreak >nul

REM Start BlackArch Tools API in new window  
echo [2/3] Starting BlackArch Tools API (Port 8080)...
start "R3ALER - BlackArch API" cmd /k "cd Tools && call ..\blackarch_venv\Scripts\activate.bat && python blackarch_web_app.py"
timeout /t 3 /nobreak >nul

REM Start Backend Server in new window
echo [3/3] Starting Node.js Backend Server (Port 3000)...
start "R3ALER - Backend Server" cmd /k "cd application\Backend && set NODE_ENV=production && npm start"

echo.
echo ============================================================
echo All R3ALER AI services started!
echo ============================================================
echo   - Knowledge API:     http://localhost:5001
echo   - BlackArch Tools:   http://localhost:8081
echo   - Backend Server:    http://localhost:3000
echo   - Frontend (Web):    http://localhost:3000
echo ============================================================
echo.
echo Services are running in separate windows.
echo Close the windows to stop the services.
pause
