-- Active: 1762569176384@@127.0.0.1@5432@postgres@public
#!/bin/bash

echo "🧪 Testing BitXtractor Endpoint"
echo "================================"

echo "Testing /api/bitxtractor/start endpoint..."
response=$(curl -s -X POST \
  -H "Content-Type: application/json" \
  -d '{"wallet_path":"/test/wallet.dat"}' \
  http://localhost:3002/api/bitxtractor/start)

echo "Response: $response"

if [[ $response == *"job_id"* ]]; then
  echo "✅ BitXtractor endpoint is working!"
else
  echo "❌ BitXtractor endpoint failed"
  echo "Full response: $response"
fi