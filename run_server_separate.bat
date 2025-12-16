@echo off
title R3ALER-AI BlackArch Web Server
echo Starting R3ALER-AI BlackArch Web Interface in separate terminal...
echo This window will remain open to keep the server running.
echo.
wsl bash -c "cd '/mnt/c/Users/work8/OneDrive/Desktop/r3al3rai/New Folder 1/R3al3r-AI Main Working/R3aler-ai/R3aler-ai' && source blackarch_venv/bin/activate && python3 Tools/simple_web_app.py"
echo.
echo Server stopped. Press any key to close this window.
pause > nul