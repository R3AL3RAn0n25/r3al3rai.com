#!/bin/bash
echo "=== Registering available tools in BlackArch ==="

# List of tools to check and register
tools=("nmap" "wireshark" "curl" "wget")

for tool in "${tools[@]}"
do
    echo "Registering $tool..."
    response=$(curl -s -X POST http://localhost:8081/api/install/$tool)
    echo "$response"
    echo ""
done

echo "=== Registration complete ==="
echo ""
echo "Testing nmap execution..."
curl -s -X POST http://localhost:8081/api/execute/nmap \
  -H 'Content-Type: application/json' \
  -d '{"args":["--version"]}' | head -c 500
echo ""
