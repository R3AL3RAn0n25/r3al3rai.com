#!/bin/bash

# R3AL3R AI - Stop All Services in WSL

if [ -f ".service_pids" ]; then
    source .service_pids
    
    echo "🛑 Stopping R3AL3R AI Services..."
    
    [ ! -z "$STORAGE_PID" ] && kill -TERM $STORAGE_PID 2>/dev/null && echo "  Stopped Storage Facility (PID: $STORAGE_PID)"
    [ ! -z "$KNOWLEDGE_PID" ] && kill -TERM $KNOWLEDGE_PID 2>/dev/null && echo "  Stopped Knowledge API (PID: $KNOWLEDGE_PID)"
    [ ! -z "$INTELLIGENCE_PID" ] && kill -TERM $INTELLIGENCE_PID 2>/dev/null && echo "  Stopped Intelligence API (PID: $INTELLIGENCE_PID)"
    [ ! -z "$DROID_PID" ] && kill -TERM $DROID_PID 2>/dev/null && echo "  Stopped Droid API (PID: $DROID_PID)"
    [ ! -z "$USER_AUTH_PID" ] && kill -TERM $USER_AUTH_PID 2>/dev/null && echo "  Stopped User Auth API (PID: $USER_AUTH_PID)"
    [ ! -z "$BACKEND_PID" ] && kill -TERM $BACKEND_PID 2>/dev/null && echo "  Stopped Backend Server (PID: $BACKEND_PID)"
    [ ! -z "$MANAGEMENT_PID" ] && kill -TERM $MANAGEMENT_PID 2>/dev/null && echo "  Stopped Management API (PID: $MANAGEMENT_PID)"
    
    rm .service_pids
    echo "✅ All services stopped"
else
    echo "⚠️  No service PIDs found. Services may not be running."
    
    # Fallback: kill by port
    echo "Attempting to stop services by port..."
    fuser -k 3000/tcp 2>/dev/null && echo "  Killed process on port 3000"
    fuser -k 3003/tcp 2>/dev/null && echo "  Killed process on port 3003"
    fuser -k 5004/tcp 2>/dev/null && echo "  Killed process on port 5004"
    fuser -k 5005/tcp 2>/dev/null && echo "  Killed process on port 5005"
    fuser -k 5006/tcp 2>/dev/null && echo "  Killed process on port 5006"
    fuser -k 5010/tcp 2>/dev/null && echo "  Killed process on port 5010"
    fuser -k 5000/tcp 2>/dev/null && echo "  Killed process on port 5000"
fi

