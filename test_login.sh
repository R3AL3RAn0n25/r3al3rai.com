#!/bin/bash
# Test login functionality

echo "=== Testing R3ALER AI Login System ==="
echo ""

# Test 1: Register a new user
UNIQUE_USER="testuser_$(date +%s)"
echo "1. Registering new user: $UNIQUE_USER..."
REGISTER_RESPONSE=$(curl -s -X POST \
  -H "Content-Type: application/json" \
  -d "{\"username\":\"$UNIQUE_USER\",\"password\":\"test123\"}" \
  http://localhost:3000/api/auth/register)

echo "$REGISTER_RESPONSE" | python3 -m json.tool
echo ""

# Test 2: Login with the user
echo "2. Logging in as $UNIQUE_USER..."
LOGIN_RESPONSE=$(curl -s -X POST \
  -H "Content-Type: application/json" \
  -d "{\"username\":\"$UNIQUE_USER\",\"password\":\"test123\"}" \
  http://localhost:3000/api/auth/login)

echo "$LOGIN_RESPONSE" | python3 -m json.tool
TOKEN=$(echo "$LOGIN_RESPONSE" | python3 -c "import json,sys; data=json.load(sys.stdin); print(data.get('token',''))")
echo ""

# Test 3: Access protected endpoint with token
if [ -n "$TOKEN" ]; then
    echo "3. Testing protected endpoint with JWT token..."
    curl -s -H "Authorization: Bearer $TOKEN" \
      http://localhost:3000/api/roles | python3 -m json.tool | head -20
    echo ""
    echo "✅ Login system is working!"
else
    echo "❌ Login failed - no token received"
fi
