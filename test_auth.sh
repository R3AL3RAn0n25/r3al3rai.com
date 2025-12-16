#!/bin/bash

echo "=== Testing R3ALER AI Authentication ==="
echo ""

# Test registration
echo "1. Testing Registration..."
REGISTER_RESPONSE=$(curl -s -X POST http://localhost:3000/api/auth/register \
  -H 'Content-Type: application/json' \
  -d '{"username":"testuser123","password":"testpass123","email":"test@example.com"}')

echo "Register Response: $REGISTER_RESPONSE"
echo ""

# Test login
echo "2. Testing Login..."
LOGIN_RESPONSE=$(curl -s -X POST http://localhost:3000/api/auth/login \
  -H 'Content-Type: application/json' \
  -d '{"username":"testuser123","password":"testpass123"}')

echo "Login Response: $LOGIN_RESPONSE"
echo ""

# Extract token if login successful
TOKEN=$(echo $LOGIN_RESPONSE | grep -o '"token":"[^"]*"' | cut -d'"' -f4)

if [ ! -z "$TOKEN" ]; then
    echo "3. Token received: ${TOKEN:0:20}..."
    echo ""
    
    # Test authenticated endpoint
    echo "4. Testing authenticated endpoint..."
    AUTH_TEST=$(curl -s http://localhost:3000/api/blackarch/tools \
      -H "Authorization: Bearer $TOKEN")
    echo "Auth Test Response (first 200 chars): ${AUTH_TEST:0:200}..."
else
    echo "Login failed - no token received"
fi

echo ""
echo "=== Test Complete ==="
