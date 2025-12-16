
# R3AL3R AI - HTTPS Setup Script
# Run this script to prepare for HTTPS deployment

Write-Host "`n================================================================" -ForegroundColor Cyan
Write-Host "          R3AL3R AI - HTTPS DEPLOYMENT SETUP" -ForegroundColor Cyan
Write-Host "================================================================`n" -ForegroundColor Cyan

$ProjectRoot = $PSScriptRoot
$CertsSource = "C:\Users\work8\OneDrive\Desktop\_.r3al3rai.com_ssl_certificate_INTERMEDIATE"
$CertsDir = Join-Path $ProjectRoot "certs"

# Step 1: Create certs directory
Write-Host "[1/6] Creating certificates directory..." -ForegroundColor Yellow
if (-not (Test-Path $CertsDir)) {
    New-Item -ItemType Directory -Path $CertsDir -Force | Out-Null
    Write-Host "  ✓ Created: $CertsDir" -ForegroundColor Green
}
else {
    Write-Host "  ✓ Directory exists: $CertsDir" -ForegroundColor Green
}

# Step 2: Copy certificate files
Write-Host "`n[2/6] Copying SSL certificates..." -ForegroundColor Yellow
if (Test-Path $CertsSource) {
    Copy-Item "$CertsSource\*" -Destination $CertsDir -Force
    Write-Host "  ✓ Copied certificates from $CertsSource" -ForegroundColor Green
    Get-ChildItem $CertsDir | ForEach-Object {
        Write-Host "    - $($_.Name)" -ForegroundColor Gray
    }
}
else {
    Write-Host "  ✗ Source not found: $CertsSource" -ForegroundColor Red
}

# Step 3: Check for private key
Write-Host "`n[3/6] Checking for private key..." -ForegroundColor Yellow
$privateKeyFiles = Get-ChildItem $CertsDir -Filter "*.key" -ErrorAction SilentlyContinue
if ($privateKeyFiles.Count -gt 0) {
    Write-Host "  ✓ Private key found: $($privateKeyFiles[0].Name)" -ForegroundColor Green
    $hasPrivateKey = $true
}
else {
    Write-Host "  ✗ PRIVATE KEY NOT FOUND!" -ForegroundColor Red
    Write-Host "`n  YOU NEED THE PRIVATE KEY FILE (.key) TO ENABLE HTTPS" -ForegroundColor Yellow
    Write-Host "  Please download it from your SSL provider and save as:" -ForegroundColor Yellow
    Write-Host "    $CertsDir\r3al3rai.com.key`n" -ForegroundColor White
    $hasPrivateKey = $false
}

# Step 4: Create certificate chain
Write-Host "`n[4/6] Creating certificate chain..." -ForegroundColor Yellow
$certFile = Join-Path $CertsDir "r3al3rai.com_ssl_certificate.cer"
$int1File = Join-Path $CertsDir "intermediate1.cer"
$int2File = Join-Path $CertsDir "intermediate2.cer"
$fullchainFile = Join-Path $CertsDir "fullchain.pem"

if ((Test-Path $certFile) -and (Test-Path $int1File) -and (Test-Path $int2File)) {
    Get-Content $certFile, $int1File, $int2File | Set-Content $fullchainFile
    Write-Host "  ✓ Created fullchain.pem" -ForegroundColor Green
}
else {
    Write-Host "  ✗ Missing certificate files" -ForegroundColor Red
}

# Step 5: Convert .cer to .pem if needed
Write-Host "`n[5/6] Converting certificates to PEM format..." -ForegroundColor Yellow
$cerFiles = @(Get-ChildItem $CertsDir -Filter "*.cer" -ErrorAction SilentlyContinue)
if ($cerFiles.Count -gt 0) {
    foreach ($cerFile in $cerFiles) {
        $pemFile = $cerFile.FullName -replace '\.cer$', '.pem'
        Copy-Item $cerFile.FullName -Destination $pemFile -Force
        Write-Host "  ✓ $($cerFile.Name) → $([System.IO.Path]::GetFileName($pemFile))" -ForegroundColor Green
    }
}
else {
    Write-Host "  ⚠ No .cer files to convert" -ForegroundColor Yellow
}

# Step 6: Check Nginx installation
Write-Host "`n[6/6] Checking Nginx installation..." -ForegroundColor Yellow
if (Test-Path "C:\nginx\nginx.exe") {
    Write-Host "  ✓ Nginx installed at C:\nginx" -ForegroundColor Green
    
    # Copy nginx config
    $nginxConfig = Join-Path $ProjectRoot "nginx-r3al3rai.conf"
    if (Test-Path $nginxConfig) {
        Copy-Item $nginxConfig -Destination "C:\nginx\conf\nginx.conf" -Force
        Write-Host "  ✓ Nginx config updated" -ForegroundColor Green
    }
}
else {
    Write-Host "  ✗ Nginx not installed" -ForegroundColor Yellow
    Write-Host "`n  TO INSTALL NGINX:" -ForegroundColor Yellow
    Write-Host "  1. Download: https://nginx.org/en/download.html" -ForegroundColor White
    Write-Host "  2. Extract to C:\nginx" -ForegroundColor White
    Write-Host "  3. Copy nginx-r3al3rai.conf to C:\nginx\conf\nginx.conf" -ForegroundColor White
    Write-Host "  4. Start: cd C:\nginx; .\nginx.exe`n" -ForegroundColor White
}

# Summary
Write-Host "`n================================================================" -ForegroundColor Cyan
Write-Host "                    SETUP SUMMARY" -ForegroundColor Cyan
Write-Host "================================================================`n" -ForegroundColor Cyan

if (Test-Path $fullchainFile) {
    Write-Host "✅ Certificate Chain: READY" -ForegroundColor Green
} else {
    Write-Host "❌ Certificate Chain: NOT CREATED" -ForegroundColor Red
}

if ($hasPrivateKey) {
    Write-Host "✅ Private Key: FOUND" -ForegroundColor Green
} else {
    Write-Host "❌ Private Key: MISSING" -ForegroundColor Red
}

if (Test-Path "C:\nginx\nginx.exe") {
    Write-Host "✅ Nginx: INSTALLED" -ForegroundColor Green
} else {
    Write-Host "⚠️  Nginx: NOT INSTALLED" -ForegroundColor Yellow
}

Write-Host "`n================================================================" -ForegroundColor Cyan
Write-Host "                    NEXT STEPS" -ForegroundColor Cyan
Write-Host "================================================================`n" -ForegroundColor Cyan

if (-not $hasPrivateKey) {
    Write-Host "1. URGENT: Download private key from SSL provider" -ForegroundColor Yellow
    Write-Host "   Save as: $CertsDir\r3al3rai.com.key`n" -ForegroundColor White
}

if (-not (Test-Path "C:\nginx\nginx.exe")) {
    Write-Host "2. Install Nginx for Windows" -ForegroundColor Yellow
    Write-Host "   Download: https://nginx.org/download/nginx-1.24.0.zip`n" -ForegroundColor White
}

Write-Host "3. Update DNS to point r3al3rai.com to your server IP" -ForegroundColor Yellow
Write-Host "4. Configure Windows Firewall for port 443" -ForegroundColor Yellow
Write-Host "5. Start Nginx: cd C:\nginx; .\nginx.exe" -ForegroundColor Yellow
Write-Host "6. Test: https://r3al3rai.com`n" -ForegroundColor Yellow

Write-Host "================================================================`n" -ForegroundColor Cyan
Write-Host "Press any key to continue..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
