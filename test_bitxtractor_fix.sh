#!/bin/bash

echo "🧪 Testing BitXtractor URL Fix"
echo "=============================="

# Test the exact URL pattern that was failing
echo "Testing direct /bitxtractor endpoint with query params..."

# Create a test wallet path (URL encoded)
WALLET_PATH="C%3A%5CUsers%5Cwork8%5COneDrive%5CDesktop%5C1.21%2B-%2BCopy.dat"

# Test the endpoint
response=$(curl -s "http://localhost:3000/bitxtractor?wallet_path=%22${WALLET_PATH}%22&currency=BTC&mode=dry&iterations=&kdf=pbkdf2&pbkdf2_hash=sha256&cipher=aes-256-cbc&extra_args=")

echo "Response: $response"

if [[ $response == *"job_id"* ]]; then
  echo "✅ BitXtractor endpoint is now working!"
else
  echo "❌ Still having issues"
  echo "Full response: $response"
fi