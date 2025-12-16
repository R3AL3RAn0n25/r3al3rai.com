#!/bin/bash

echo "🚀 COMPLETE BITXTRACTOR FUNCTIONALITY TEST"
echo "=========================================="

echo "Testing with actual wallet: C:\\Users\\work8\\OneDrive\\Desktop\\1.21.dat"

# Test the corrected BitXtractor endpoint with the real wallet
response=$(curl -s -X POST \
  -H "Content-Type: application/json" \
  -d '{
    "wallet_path": "C:\\Users\\work8\\OneDrive\\Desktop\\1.21.dat",
    "mode": "dry",
    "kdf": "pbkdf2",
    "pbkdf2_hash": "sha256",
    "cipher": "aes-256-cbc"
  }' \
  http://localhost:3002/api/bitxtractor/start)

echo "BitXtractor Response:"
echo "$response"

# Extract job_id if successful
if [[ $response == *"job_id"* ]]; then
  job_id=$(echo "$response" | grep -o '"job_id":"[^"]*"' | cut -d'"' -f4)
  echo ""
  echo "✅ BitXtractor started successfully!"
  echo "Job ID: $job_id"
  
  echo ""
  echo "Waiting for processing..."
  sleep 3
  
  echo ""
  echo "Checking job status..."
  status_response=$(curl -s "http://localhost:3002/api/bitxtractor/status/$job_id")
  echo "Status: $status_response"
  
  # Wait a bit more and check again
  sleep 3
  echo ""
  echo "Final status check..."
  final_status=$(curl -s "http://localhost:3002/api/bitxtractor/status/$job_id")
  echo "Final Status: $final_status"
  
else
  echo "❌ BitXtractor failed to start"
  echo "Response: $response"
fi