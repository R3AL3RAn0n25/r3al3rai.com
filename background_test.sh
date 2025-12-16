#!/bin/bash

echo "🚀 BACKGROUND BITXTRACTOR TEST - $(date)" > /tmp/bitxtractor_test_results.txt
echo "=======================================" >> /tmp/bitxtractor_test_results.txt

echo "Testing with wallet: C:\\Users\\work8\\OneDrive\\Desktop\\1.21.dat" >> /tmp/bitxtractor_test_results.txt

# Test the corrected BitXtractor endpoint
response=$(curl -s -X POST \
  -H "Content-Type: application/json" \
  -d '{
    "wallet_path": "C:\\Users\\work8\\OneDrive\\Desktop\\1.21.dat",
    "mode": "dry",
    "kdf": "pbkdf2",
    "pbkdf2_hash": "sha256",
    "cipher": "aes-256-cbc"
  }' \
  http://localhost:3002/api/bitxtractor/start 2>&1)

echo "" >> /tmp/bitxtractor_test_results.txt
echo "BitXtractor Start Response:" >> /tmp/bitxtractor_test_results.txt
echo "$response" >> /tmp/bitxtractor_test_results.txt

# Extract job_id if successful
if [[ $response == *"job_id"* ]]; then
  job_id=$(echo "$response" | grep -o '"job_id":"[^"]*"' | cut -d'"' -f4)
  echo "" >> /tmp/bitxtractor_test_results.txt
  echo "✅ BitXtractor started successfully!" >> /tmp/bitxtractor_test_results.txt
  echo "Job ID: $job_id" >> /tmp/bitxtractor_test_results.txt
  
  echo "" >> /tmp/bitxtractor_test_results.txt
  echo "Waiting 5 seconds for processing..." >> /tmp/bitxtractor_test_results.txt
  sleep 5
  
  echo "" >> /tmp/bitxtractor_test_results.txt
  echo "Checking job status..." >> /tmp/bitxtractor_test_results.txt
  status_response=$(curl -s "http://localhost:3002/api/bitxtractor/status/$job_id" 2>&1)
  echo "Status: $status_response" >> /tmp/bitxtractor_test_results.txt
  
  # Wait more and final check
  sleep 5
  echo "" >> /tmp/bitxtractor_test_results.txt
  echo "Final status check..." >> /tmp/bitxtractor_test_results.txt
  final_status=$(curl -s "http://localhost:3002/api/bitxtractor/status/$job_id" 2>&1)
  echo "Final Status: $final_status" >> /tmp/bitxtractor_test_results.txt
  
else
  echo "❌ BitXtractor failed to start" >> /tmp/bitxtractor_test_results.txt
  echo "Error Response: $response" >> /tmp/bitxtractor_test_results.txt
fi

echo "" >> /tmp/bitxtractor_test_results.txt
echo "Test completed at $(date)" >> /tmp/bitxtractor_test_results.txt
echo "Results saved to /tmp/bitxtractor_test_results.txt" >> /tmp/bitxtractor_test_results.txt