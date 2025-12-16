#!/bin/bash
# Test tool execution
curl -s -X POST http://localhost:8081/api/execute/nmap \
  -H 'Content-Type: application/json' \
  -d '{"args":["--version"]}'
