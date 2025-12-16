#!/bin/bash

# R3AL3R AI - Check Service Status

echo "🔍 R3AL3R AI Service Status"
echo "============================"
echo ""

services=(
    "Backend:3000"
    "Storage:3003"
    "Knowledge:5004"
    "Intelligence:5010"
    "Droid:5005"
    "User Auth:5006"
    "Management:5000"
)

running=0
total=${#services[@]}

for service in "${services[@]}"; do
    name="${service%:*}"
    port="${service#*:}"
    
    if nc -z localhost $port 2>/dev/null; then
        echo "✅ $name (Port $port): RUNNING"
        ((running++))
    else
        echo "❌ $name (Port $port): OFFLINE"
    fi
done

echo ""
echo "Services: $running/$total running"

# Check database
if sudo service postgresql status | grep -q "online"; then
    echo "✅ PostgreSQL: RUNNING"
else
    echo "❌ PostgreSQL: OFFLINE"
fi

