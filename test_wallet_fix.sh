#!/bin/bash

echo "🧪 Testing Wallet Extractor Fix"
echo "================================"

cd '/mnt/c/Users/work8/OneDrive/Desktop/r3al3rai/New Folder 1/R3al3r-AI Main Working/R3aler-ai/R3aler-ai'
source blackarch_venv/bin/activate

echo "Running wallet extractor with test parameters..."

# Test the exact command that was failing (with a dry run for safety)
python Tools/tools/wallet_extractor.py \
  --wallet "C:\\Users\\work8\\OneDrive\\Desktop\\1.21 - Copy.dat" \
  --dry-run \
  --json \
  --kdf pbkdf2 \
  --pbkdf2-hash sha256 \
  --cipher aes-256-cbc

echo "Test complete!"