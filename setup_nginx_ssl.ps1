<#
setup_nginx_ssl.ps1

Copies provided certificate files into the local nginx distribution, verifies a private key
is present (or stops and requests it), updates the repository `nginx.conf` paths to point
at `C:\nginx\conf\certs\`, sets permissive but reviewable ACLs so nginx can read the
private key, runs `nginx -t` and reloads nginx if tests pass.

USAGE (run as Administrator):
  powershell -ExecutionPolicy Bypass -File .\setup_nginx_ssl.ps1

This script is conservative: it will NOT attempt to extract a private key from a PFX.
If your private key is inside a .pfx, export the key to a .key first and re-run the script,
or tell me and I can add PFX export steps (requires OpenSSL or certutil guidance).
#>

param(
  [string]$NginxRoot = 'C:\nginx',
  [string]$CertSource = 'C:\Users\work8\OneDrive\Desktop\r3al3rai.com_ssl_certificate.cer',
  [string]$IntermediateSource = 'C:\Users\work8\OneDrive\Desktop\intermediate1.cer',
  [string]$PreferredKeyPattern = 'C:\Users\work8\OneDrive\Desktop\r3al3r*.*'
)

function Write-Section($t){ Write-Output "`n--- $t ---`n" }

Write-Output "Running setup_nginx_ssl.ps1: will copy cert(s) into $NginxRoot\conf\certs and update config"
Write-Section "Sanity checks"
if (-not (Test-Path $NginxRoot)) { Write-Output "Warning: nginx root not found at $NginxRoot. Adjust -NginxRoot or install nginx there." }

Write-Output "Cert source exists: $(Test-Path $CertSource)"
Write-Output "Intermediate exists: $(Test-Path $IntermediateSource)"

Write-Section "Locate private key"
# look for common private key files near OneDrive or repo root
$candidates = Get-ChildItem -Path (Split-Path $PreferredKeyPattern) -Filter (Split-Path $PreferredKeyPattern -Leaf) -File -ErrorAction SilentlyContinue
if (-not $candidates) {
  $searchPaths = @(
    'C:\Users\work8\OneDrive\Desktop',
    (Get-Location).Path
  )
  foreach ($p in $searchPaths) {
    $candidates += Get-ChildItem -Path $p -Recurse -Include '*.key','*.pem','*.pfx' -File -ErrorAction SilentlyContinue
  }
}

if ($candidates) {
  Write-Output "Found potential key files (choose one by index if multiple):"
  $i = 0
  $candidates | ForEach-Object { Write-Output "[$i] $($_.FullName)"; $i++ }
  $chosen = $candidates | Select-Object -First 1
  Write-Output "Auto-selecting first candidate: $($chosen.FullName)"
  $keyPath = $chosen.FullName
} else {
  Write-Output "No private key file (.key/.pem/.pfx) found nearby. Please place your private key (e.g. r3al3r-key-new6.key) in your OneDrive Desktop folder and re-run this script."
  Write-Output "I cannot complete TLS setup without the private key. Exiting."
  exit 2
}

if ($keyPath -like '*.pfx') {
  Write-Output "Found a PFX file at $keyPath — this script will not auto-extract the private key."
  Write-Output "Please export the certificate and private key to separate files (.crt/.key) and re-run, or ask me to add PFX extraction steps. Exiting."
  exit 3
}

Write-Section "Copy files into nginx conf/certs"
$destDir = Join-Path $NginxRoot 'conf\certs'
New-Item -Path $destDir -ItemType Directory -Force | Out-Null

if (Test-Path $CertSource) {
  $certDest = Join-Path $destDir (Split-Path $CertSource -Leaf)
  Copy-Item -Path $CertSource -Destination $certDest -Force
  Write-Output "Copied cert: $certDest"
} else { Write-Output "Certificate source not found at $CertSource — please confirm path." }

if (Test-Path $IntermediateSource) {
  $interDest = Join-Path $destDir (Split-Path $IntermediateSource -Leaf)
  Copy-Item -Path $IntermediateSource -Destination $interDest -Force
  Write-Output "Copied intermediate: $interDest"
}

if (Test-Path $keyPath) {
  # Normalize the private key filename to the expected nginx name for the repo config
  $keyDestName = 'r3al3rai.com.key'
  $keyDest = Join-Path $destDir $keyDestName
  Copy-Item -Path $keyPath -Destination $keyDest -Force
  Write-Output "Copied key to: $keyDest"
} else { Write-Output "Selected key path $keyPath not present at copy time." }

Write-Section "Set ACLs (temporary permissive - please tighten later)"
# Try to determine the nginx executable and process owner. Use WMI to get the owner if possible.
$nginxExe = Join-Path $NginxRoot 'nginx.exe'
$nginxProcess = Get-Process -Name nginx -ErrorAction SilentlyContinue | Select-Object -First 1
if ($nginxProcess) {
  $pid = $nginxProcess.Id
  $procWmi = Get-WmiObject -Class Win32_Process -Filter "ProcessId = $pid" -ErrorAction SilentlyContinue
  if ($procWmi) {
    $ownerInfo = $procWmi.GetOwner()
    $nginxOwner = "$($ownerInfo.Domain)\$($ownerInfo.User)"
    Write-Output "Detected nginx running as: $nginxOwner"
    $grantArg = "$($nginxOwner):(R)"
    & icacls "$destDir\*" /grant $grantArg /C | Out-Null
    Write-Output "Granted read to $nginxOwner on certs folder"
  } else {
    Write-Output "Could not determine nginx owner via WMI; granting read to 'Users' group temporarily."
    & icacls "$destDir\*" /grant 'Users:(R)' /C | Out-Null
  }
} else {
  Write-Output "nginx not running - granting read to 'Users' group temporarily. Start nginx and adjust ACLs to the exact service user later."
  & icacls "$destDir\*" /grant 'Users:(R)' /C | Out-Null
}

Write-Section "Update repo nginx.conf to use nginx conf/certs paths"
# Update the repository nginx.conf in-place (this file in repo) to reference certs in $NginxRoot\conf\certs
$repoNginx = Join-Path (Split-Path -Parent $MyInvocation.MyCommand.Path) 'nginx.conf'
if (-not (Test-Path $repoNginx)) { $repoNginx = Join-Path (Get-Location) 'nginx.conf' }
if (Test-Path $repoNginx) {
  # determine which .cer file we copied into destDir
  $certFile = (Get-ChildItem -Path $destDir -Filter '*.cer' -File -ErrorAction SilentlyContinue | Select-Object -First 1)
  if ($certFile) { $certPath = $certFile.FullName } else { $certPath = Join-Path $destDir (Split-Path $CertSource -Leaf) }
  $keyPath = $keyDest
  $content = Get-Content $repoNginx -Raw
  $content = $content -replace 'ssl_certificate\s+".*?";','ssl_certificate "' + $certPath + '";'
  $content = $content -replace 'ssl_certificate_key\s+".*?";','ssl_certificate_key "' + $keyPath + '";'
  Set-Content -Path $repoNginx -Value $content -Encoding UTF8
  Write-Output "Updated repository nginx.conf at $repoNginx"
} else { Write-Output "Repository nginx.conf not found; skip updating it." }

Write-Section "nginx test and reload"
if (Test-Path $nginxExe) {
  & $nginxExe -t 2>&1 | ForEach-Object { Write-Output "  $_" }
  $testOutput = & $nginxExe -t 2>&1
  $testOk = $testOutput -match 'test is successful|configuration file .* test is successful'
  if ($testOk) {
    Write-Output "nginx config test OK - reloading nginx"
    & $nginxExe -s reload
  } else { Write-Output "nginx test failed - inspect output above and correct paths/permissions." }
} else {
  Write-Output "Could not locate nginx.exe at $nginxExe. Start nginx manually and verify config." 
}

Write-Output "Done. If TLS still fails, paste the exact 'nginx -t' output here and I'll help fix it."
