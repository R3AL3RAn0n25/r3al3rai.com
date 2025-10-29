param(
    [Parameter(Mandatory=$true)]
    [string]$ServerIP
)

Write-Host "Testing all R3ALER AI endpoints on $ServerIP"

# Test main page
Write-Host "`n=== Testing Main Page ==="
try {
    $response = Invoke-WebRequest -Uri "http://$ServerIP" -UseBasicParsing
    Write-Host "✓ Main page loads (Status: $($response.StatusCode))"
} catch {
    Write-Host "✗ Main page failed: $($_.Exception.Message)"
}

# Test registration endpoint
Write-Host "`n=== Testing Registration ==="
$regData = @{
    full_name = "Test User"
    date_of_birth = "1990-01-01"
    email = "test@example.com"
    username = "testuser"
    password = "testpass123"
} | ConvertTo-Json

try {
    $response = Invoke-RestMethod -Uri "http://$ServerIP/api/auth/register" -Method POST -Body $regData -ContentType "application/json"
    Write-Host "✓ Registration works: $($response | ConvertTo-Json)"
} catch {
    Write-Host "✗ Registration failed: $($_.Exception.Message)"
}

# Test login endpoint
Write-Host "`n=== Testing Login ==="
$loginData = @{
    username = "testuser"
    password = "testpass123"
} | ConvertTo-Json

try {
    $response = Invoke-RestMethod -Uri "http://$ServerIP/api/auth/login" -Method POST -Body $loginData -ContentType "application/json"
    Write-Host "✓ Login works: $($response | ConvertTo-Json)"
} catch {
    Write-Host "✗ Login failed: $($_.Exception.Message)"
}

# Test chat endpoint
Write-Host "`n=== Testing Chat ==="
$chatData = @{
    message = "Hello AI"
} | ConvertTo-Json

try {
    $response = Invoke-RestMethod -Uri "http://$ServerIP/api/chat" -Method POST -Body $chatData -ContentType "application/json"
    Write-Host "✓ Chat works: $($response | ConvertTo-Json)"
} catch {
    Write-Host "✗ Chat failed: $($_.Exception.Message)"
}

Write-Host "`n=== Testing Static Files ==="
$staticFiles = @("/static/js/app.js", "/static/css/style.css", "/static/js/matrix_face.js")
foreach ($file in $staticFiles) {
    try {
        $response = Invoke-WebRequest -Uri "http://$ServerIP$file" -UseBasicParsing
        Write-Host "✓ $file loads (Status: $($response.StatusCode))"
    } catch {
        Write-Host "✗ $file failed: $($_.Exception.Message)"
    }
}