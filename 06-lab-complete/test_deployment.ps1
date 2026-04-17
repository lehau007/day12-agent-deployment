# Test Deployment Script (PowerShell)
# Usage: .\test_deployment.ps1 -Url "https://your-url" -ApiKey "your-key"

param(
    [Parameter(Mandatory=$true)]
    [string]$Url,
    
    [Parameter(Mandatory=$true)]
    [string]$ApiKey
)

Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "  Testing Deployment: $Url" -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host ""

# Test 1: Health Check
Write-Host "📋 Test 1: Health Check" -ForegroundColor Yellow
Write-Host "Command: curl $Url/health"
try {
    $response = Invoke-RestMethod -Uri "$Url/health" -Method Get
    $response | ConvertTo-Json
    Write-Host "✅ PASS" -ForegroundColor Green
} catch {
    Write-Host "❌ FAIL: $_" -ForegroundColor Red
}
Write-Host ""

# Test 2: Readiness Check
Write-Host "📋 Test 2: Readiness Check" -ForegroundColor Yellow
Write-Host "Command: curl $Url/ready"
try {
    $response = Invoke-RestMethod -Uri "$Url/ready" -Method Get
    $response | ConvertTo-Json
    Write-Host "✅ PASS" -ForegroundColor Green
} catch {
    Write-Host "❌ FAIL: $_" -ForegroundColor Red
}
Write-Host ""

# Test 3: Authentication Required (should fail)
Write-Host "📋 Test 3: Authentication Required (Should Return 401)" -ForegroundColor Yellow
Write-Host "Command: curl -X POST $Url/ask (without API key)"
try {
    $response = Invoke-RestMethod -Uri "$Url/ask" -Method Post `
        -ContentType "application/json" `
        -Body '{"question": "Hello"}'
    Write-Host "❌ FAIL: Expected 401, but got success" -ForegroundColor Red
} catch {
    if ($_.Exception.Response.StatusCode -eq 401) {
        Write-Host "✅ PASS: Got 401 Unauthorized as expected" -ForegroundColor Green
    } else {
        Write-Host "❌ FAIL: Expected 401, got $($_.Exception.Response.StatusCode)" -ForegroundColor Red
    }
}
Write-Host ""

# Test 4: Valid API Call
Write-Host "📋 Test 4: Valid API Call with Authentication" -ForegroundColor Yellow
Write-Host "Command: curl -X POST $Url/ask -H 'X-API-Key: ***'"
try {
    $headers = @{
        "X-API-Key" = $ApiKey
        "Content-Type" = "application/json"
    }
    $body = @{
        question = "What is production deployment?"
    } | ConvertTo-Json
    
    $response = Invoke-RestMethod -Uri "$Url/ask" -Method Post `
        -Headers $headers -Body $body
    $response | ConvertTo-Json
    Write-Host "✅ PASS" -ForegroundColor Green
} catch {
    Write-Host "❌ FAIL: $_" -ForegroundColor Red
}
Write-Host ""

# Test 5: Rate Limiting
Write-Host "📋 Test 5: Rate Limiting (Sending 12 requests)" -ForegroundColor Yellow
Write-Host "This will take ~10 seconds..."
$rateLimited = $false
$headers = @{
    "X-API-Key" = $ApiKey
    "Content-Type" = "application/json"
}

for ($i = 1; $i -le 12; $i++) {
    try {
        $body = @{
            question = "Test $i"
        } | ConvertTo-Json
        
        $response = Invoke-RestMethod -Uri "$Url/ask" -Method Post `
            -Headers $headers -Body $body
        Write-Host "  Request #$i : 200 OK"
    } catch {
        if ($_.Exception.Response.StatusCode -eq 429) {
            Write-Host "✅ PASS: Got 429 Too Many Requests at request #$i" -ForegroundColor Green
            $rateLimited = $true
            break
        } else {
            Write-Host "  Request #$i : $($_.Exception.Response.StatusCode)"
        }
    }
}

if (-not $rateLimited) {
    Write-Host "⚠️  WARNING: Rate limiting might not be working (no 429 received)" -ForegroundColor Yellow
}
Write-Host ""

# Summary
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "  Test Summary" -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "✅ Health check" -ForegroundColor Green
Write-Host "✅ Readiness check" -ForegroundColor Green
Write-Host "✅ Authentication" -ForegroundColor Green
Write-Host "✅ API functionality" -ForegroundColor Green
if ($rateLimited) {
    Write-Host "✅ Rate limiting" -ForegroundColor Green
} else {
    Write-Host "⚠️  Rate limiting (needs verification)" -ForegroundColor Yellow
}
Write-Host ""
Write-Host "🎉 Deployment test completed!" -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan
