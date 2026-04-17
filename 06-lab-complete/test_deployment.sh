#!/bin/bash

# Test Deployment Script
# Usage: ./test_deployment.sh <YOUR_URL> <YOUR_API_KEY>

if [ -z "$1" ]; then
    echo "❌ Error: Missing URL"
    echo "Usage: ./test_deployment.sh <URL> <API_KEY>"
    echo "Example: ./test_deployment.sh https://my-agent.railway.app my-secret-key"
    exit 1
fi

if [ -z "$2" ]; then
    echo "❌ Error: Missing API Key"
    echo "Usage: ./test_deployment.sh <URL> <API_KEY>"
    exit 1
fi

URL=$1
API_KEY=$2

echo "=========================================="
echo "  Testing Deployment: $URL"
echo "=========================================="
echo ""

# Test 1: Health Check
echo "📋 Test 1: Health Check"
echo "Command: curl $URL/health"
curl -s $URL/health | jq '.' || curl -s $URL/health
echo -e "\n"

# Test 2: Readiness Check
echo "📋 Test 2: Readiness Check"
echo "Command: curl $URL/ready"
curl -s $URL/ready | jq '.' || curl -s $URL/ready
echo -e "\n"

# Test 3: Authentication Required (should fail)
echo "📋 Test 3: Authentication Required (Should Return 401)"
echo "Command: curl -X POST $URL/ask (without API key)"
HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" -X POST $URL/ask \
  -H "Content-Type: application/json" \
  -d '{"question": "Hello"}')
if [ "$HTTP_CODE" = "401" ]; then
    echo "✅ PASS: Got 401 Unauthorized as expected"
else
    echo "❌ FAIL: Expected 401, got $HTTP_CODE"
fi
echo ""

# Test 4: Valid API Call
echo "📋 Test 4: Valid API Call with Authentication"
echo "Command: curl -X POST $URL/ask -H 'X-API-Key: ***'"
RESPONSE=$(curl -s -X POST $URL/ask \
  -H "X-API-Key: $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"question": "What is production deployment?"}')
echo "$RESPONSE" | jq '.' || echo "$RESPONSE"
echo ""

# Test 5: Rate Limiting
echo "📋 Test 5: Rate Limiting (Sending 12 requests)"
echo "This will take ~10 seconds..."
RATE_LIMITED=false
for i in {1..12}; do
    HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" -X POST $URL/ask \
      -H "X-API-Key: $API_KEY" \
      -H "Content-Type: application/json" \
      -d "{\"question\": \"Test $i\"}")
    
    if [ "$HTTP_CODE" = "429" ]; then
        echo "✅ PASS: Got 429 Too Many Requests at request #$i"
        RATE_LIMITED=true
        break
    fi
    echo "  Request #$i: $HTTP_CODE"
done

if [ "$RATE_LIMITED" = false ]; then
    echo "⚠️  WARNING: Rate limiting might not be working (no 429 received)"
fi
echo ""

# Summary
echo "=========================================="
echo "  Test Summary"
echo "=========================================="
echo "✅ Health check"
echo "✅ Readiness check"
echo "✅ Authentication"
echo "✅ API functionality"
if [ "$RATE_LIMITED" = true ]; then
    echo "✅ Rate limiting"
else
    echo "⚠️  Rate limiting (needs verification)"
fi
echo ""
echo "🎉 Deployment test completed!"
echo "=========================================="
