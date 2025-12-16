#!/bin/bash
# Test BlackArch tool execution

echo "Testing nmap execution..."
curl --max-time 60 -s -X POST \
  -H "Content-Type: application/json" \
  -d '{"args":["-V"]}' \
  http://localhost:8081/api/execute/nmap | python3 -m json.tool
