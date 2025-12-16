@echo off
REM R3AL3R-AI BlackArch Integration Startup Script for Windows
REM Easy management script for BlackArch tools integration
REM
REM Usage:
REM   start_blackarch.bat          - Start all services
REM   start_blackarch.bat web      - Start only web interface
REM   start_blackarch.bat status   - Check system status
REM   start_blackarch.bat stop     - Stop all services
REM   start_blackarch.bat install  - Install a tool
REM   start_blackarch.bat list     - List available tools

setlocal EnableDelayedExpansion

REM Configuration
set PROJECT_DIR=C:\Users\work8\OneDrive\Desktop\r3al3rai\New Folder 1\R3al3r-AI Main Working\R3aler-ai\R3aler-ai
set "WSL_PROJECT_DIR=/mnt/c/Users/work8/OneDrive/Desktop/r3al3rai/New Folder 1/R3al3r-AI Main Working/R3aler-ai/R3aler-ai"
set "VENV_PATH=%WSL_PROJECT_DIR%/blackarch_venv"
set "TOOLS_DIR=%WSL_PROJECT_DIR%/Tools"
set WEB_PORT=8081

REM Colors (Windows doesn't support colors easily, so we'll use text)
echo.
echo ===============================================
echo 🛡️  R3AL3R-AI BlackArch Integration
echo ===============================================
echo.

REM Parse command line arguments
set COMMAND=%1
if "%COMMAND%"=="" set COMMAND=start

if "%COMMAND%"=="start" goto start_all
if "%COMMAND%"=="web" goto start_web
if "%COMMAND%"=="status" goto check_status
if "%COMMAND%"=="stop" goto stop_services
if "%COMMAND%"=="list" goto list_tools
if "%COMMAND%"=="install" goto install_tool
if "%COMMAND%"=="execute" goto execute_tool
if "%COMMAND%"=="help" goto show_help
if "%COMMAND%"=="-h" goto show_help
if "%COMMAND%"=="--help" goto show_help

echo ❌ Unknown command: %COMMAND%
echo Use 'start_blackarch.bat help' for available commands
exit /b 1

:start_all
echo 🚀 Starting all BlackArch services...
echo.
echo 📊 System Status:
wsl bash -c "cd '%WSL_PROJECT_DIR%' && source %VENV_PATH%/bin/activate && python3 %TOOLS_DIR%/blackarch_tools_manager.py status | head -5"
echo.
echo 🌐 Starting web interface...
echo ✅ Access the web interface at: http://localhost:%WEB_PORT%
echo ✅ API available at: http://localhost:%WEB_PORT%/api/
echo ⚠️  Press Ctrl+C to stop all services
echo.
goto start_web

:start_web
echo 🌐 Starting BlackArch Web Interface...
wsl bash -c "cd \"%WSL_PROJECT_DIR%\" && source \"%VENV_PATH%/bin/activate\" && python3 \"%TOOLS_DIR%/blackarch_web_app.py\" --port %WEB_PORT%"
goto end

:check_status
echo 📊 Checking BlackArch System Status...
wsl bash -c "cd '%WSL_PROJECT_DIR%' && source %VENV_PATH%/bin/activate && python3 %TOOLS_DIR%/blackarch_tools_manager.py status"
echo.
echo 🌐 Web Interface Status:
wsl bash -c "curl -s http://localhost:%WEB_PORT%/api/status > /dev/null 2>&1 && echo '✅ Web interface is running on port %WEB_PORT%' || echo '❌ Web interface is not running'"
goto end

:list_tools
echo 🔧 Available BlackArch Tools:
wsl bash -c "cd '%WSL_PROJECT_DIR%' && source %VENV_PATH%/bin/activate && python3 %TOOLS_DIR%/blackarch_tools_manager.py list | head -20"
echo.
echo Showing first 20 tools. Use WSL for complete list.
goto end

:install_tool
if "%2"=="" (
    echo ❌ Please specify a tool name
    echo Usage: start_blackarch.bat install ^<tool_name^>
    echo Example: start_blackarch.bat install nmap
    exit /b 1
)
echo 📦 Installing tool: %2
wsl bash -c "cd '%WSL_PROJECT_DIR%' && source %VENV_PATH%/bin/activate && python3 %TOOLS_DIR%/blackarch_tools_manager.py install %2"
goto end

:execute_tool
if "%2"=="" (
    echo ❌ Please specify a tool name
    echo Usage: start_blackarch.bat execute ^<tool_name^> [args]
    echo Example: start_blackarch.bat execute nmap -sS 192.168.1.1
    exit /b 1
)
echo 🚀 Executing tool: %2 %3 %4 %5 %6 %7 %8 %9
wsl bash -c "cd '%WSL_PROJECT_DIR%' && source %VENV_PATH%/bin/activate && python3 %TOOLS_DIR%/blackarch_tools_manager.py execute %2 %3 %4 %5 %6 %7 %8 %9"
goto end

:stop_services
echo 🛑 Stopping BlackArch services...
REM Kill any running Python processes related to BlackArch
wsl bash -c "pkill -f blackarch_web_app.py 2>/dev/null && echo '✅ Web interface stopped' || echo '⚠️ Web interface was not running'"
echo ✅ All services stopped
goto end

:show_help
echo R3AL3R-AI BlackArch Integration Management
echo.
echo Usage: start_blackarch.bat [command] [options]
echo.
echo Commands:
echo   start           Start all services (web interface)
echo   web             Start only web interface  
echo   status          Check system status
echo   stop            Stop all services
echo   list            List available tools
echo   install ^<tool^>  Install a specific tool
echo   execute ^<tool^>  Execute a tool with arguments
echo   help            Show this help message
echo.
echo Examples:
echo   start_blackarch.bat start                    # Start all services
echo   start_blackarch.bat status                   # Check status
echo   start_blackarch.bat list                     # List tools
echo   start_blackarch.bat install nmap             # Install nmap
echo   start_blackarch.bat execute nmap -sS 192.168.1.1  # Run nmap scan
echo.
echo Web Interface: http://localhost:%WEB_PORT%
echo API Endpoints: http://localhost:%WEB_PORT%/api/
goto end

:end
echo.
echo ===============================================
pause