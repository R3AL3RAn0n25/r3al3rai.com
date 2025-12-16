#!/bin/bash

echo "🧪 R3ALER AI ENDPOINT TESTING"
echo "============================="

echo ""
echo "📡 Testing Knowledge API (Port 5001)..."
echo "Health check:"
curl -s http://localhost:5001/health
echo ""
echo "Topics endpoint:"
curl -s http://localhost:5001/api/kb/topics | head -c 200
echo ""

echo ""
echo "🛠️ Testing BlackArch/Droid API (Port 8080)..."
echo "Health check:"
curl -s http://localhost:8080/health
echo ""
echo "Droid profile test:"
curl -s http://localhost:8080/api/droid/profile/test | head -c 200
echo ""

echo ""
echo "⚙️ Testing Backend API (Port 3002)..."
echo "AI Status:"
curl -s http://localhost:3002/api/ai-status | head -c 200
echo ""

echo ""
echo "🔐 Testing BitXtractor API (Port 3002)..."
echo "BitXtractor endpoint test (expecting error without job_id):"
curl -s http://localhost:3002/api/bitxtractor/status/test | head -c 200
echo ""

echo ""
echo "🌐 Testing BlackArch Proxy (Port 3002)..."
echo "BlackArch status:"
curl -s http://localhost:3002/api/blackarch/status | head -c 200
echo ""
echo "BlackArch tools:"
curl -s http://localhost:3002/api/blackarch/tools | head -c 200
echo ""

echo ""
echo "✅ Endpoint testing complete!"